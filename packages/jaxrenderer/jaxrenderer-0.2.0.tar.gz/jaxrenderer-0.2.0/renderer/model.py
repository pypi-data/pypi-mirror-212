from functools import partial
from typing import NamedTuple, Optional, Sequence, Union

import jax
import jax.experimental.checkify as checkify
import jax.lax as lax
import jax.numpy as jnp
from jax.tree_util import tree_map
from jaxtyping import (Array, Bool, Float, Integer, Num, PyTree, Shaped,
                       jaxtyped)

from .geometry import Camera
from .types import (FALSE_ARRAY, FaceIndices, Normals, SpecularMap, Texture,
                    UVCoordinates, Vec3f, Vertices)
from .value_checker import index_in_bound

ModelMatrix = Float[Array, "4 4"]


class Model(NamedTuple):
    """Model with vertices specification and attached maps.

    NormalMap is not included for now as it is not used in the reference
    implementation
    [erwincoumans/tinyrenderer](https://github.com/erwincoumans/tinyrenderer).
    """
    verts: Vertices
    norms: Normals
    uvs: UVCoordinates
    faces: FaceIndices
    faces_norm: FaceIndices
    faces_uv: FaceIndices

    diffuse_map: Texture
    specular_map: SpecularMap

    @classmethod
    @jaxtyped
    def create(
        cls,
        verts: Vertices,
        norms: Normals,
        uvs: UVCoordinates,
        faces: FaceIndices,
        diffuse_map: Texture,
        specular_map: Optional[SpecularMap] = None,
    ) -> "Model":
        """A convenient method to create a Model assuming faces_norm and
            faces_uv are the same as faces. A default specular_map is used if
            not given, with a constant value of 2.0.
        """
        if specular_map is None:
            # reference: https://github.com/erwincoumans/tinyrenderer/blob/89e8adafb35ecf5134e7b17b71b0f825939dc6d9/model.cpp#L215
            specular_map = lax.full(diffuse_map.shape[:2], 2.0)

        assert isinstance(verts, Vertices), f"{verts}"
        assert isinstance(norms, Normals), f"{norms}"
        assert isinstance(uvs, UVCoordinates), f"{uvs}"
        assert isinstance(faces, FaceIndices), f"{faces}"
        assert isinstance(diffuse_map, Texture), f"{diffuse_map}"
        assert isinstance(specular_map, SpecularMap), f"{specular_map}"

        return cls(
            verts=verts,
            norms=norms,
            uvs=uvs,
            faces=faces,
            faces_norm=faces,
            faces_uv=faces,
            diffuse_map=diffuse_map,
            specular_map=specular_map,
        )

    @jaxtyped
    @jax.jit
    def asserts(self):
        """Asserts that all fields are of correct shape and type."""
        assert isinstance(self.verts, Vertices), f"{self.verts}"
        assert isinstance(self.norms, Normals), f"{self.norms}"
        assert isinstance(self.uvs, UVCoordinates), f"{self.uvs}"
        assert isinstance(self.faces, FaceIndices), f"{self.faces}"
        assert isinstance(self.faces_norm, FaceIndices), f"{self.faces_norm}"
        assert isinstance(self.faces_uv, FaceIndices), f"{self.faces_uv}"
        assert isinstance(self.diffuse_map, Texture), f"{self.diffuse_map}"
        assert isinstance(self.specular_map,
                          SpecularMap), f"{self.specular_map}"

    @jaxtyped
    @checkify.checkify
    @jax.jit
    def value_checks(self):
        """Check values are of correct value ranges.

        Checks implemented:
          - indices are in bound, for faces, faces_norm, faces_uv (against
            verts, norms, uv).

        UV coordinates are not checked as out-of-bound values are allowed and used as "repeat" mode.

        Usage:
          model = Model(...)
          err, _ = model.value_checks()
          err.throw()  # throw if any error is found.
        """
        # indices are in bound
        checkify.check(
            index_in_bound(self.faces, self.verts.shape[0]),
            # f-string for shape as shape is compile-time constant and
            # is not supported as a format string parameter in checkify.
            f"faces out of bound, expected [0, {self.verts.shape[0]}),"
            # separately specify fmt_kwargs in a non-f-string.
            " got {max_idx}.",
            max_idx=self.faces.max(),
        )
        checkify.check(
            index_in_bound(self.faces_norm, self.norms.shape[0]),
            f"faces_norm out of bound, expected [0, {self.norms.shape[0]}),"
            " got {max_idx}.",
            max_idx=self.faces_norm.max(),
        )
        checkify.check(
            index_in_bound(self.faces_uv, self.uvs.shape[0]),
            f"faces_uv out of bound, expected [0, {self.uvs.shape[0]}),"
            " got {max_idx}.",
            max_idx=self.faces_uv.max(),
        )


VertT = Num[Array, "_dim ..."]
VertsT = Union[list[VertT], tuple[VertT, ...]]
FaceIndicesT = Num[Array, "_faces 3"]
FaceIndicessT = Union[list[FaceIndicesT], tuple[FaceIndicesT, ...]]

MapT = Num[Array, "_width _height ..."]
MapsT = Union[list[MapT], tuple[MapT, ...]]
Shape2DT = tuple[Integer[Array, ""], Integer[Array, ""]]
"""Shape of first two components of a map, i.e., (width, height)."""


class MergedModel(NamedTuple):
    """Merged model with vertices, normals, uv coordinates, and faces."""
    verts: Vertices
    norms: Normals
    uvs: UVCoordinates
    faces: FaceIndices
    faces_norm: FaceIndices
    faces_uv: FaceIndices

    # broadcasted object info into per-vertex
    texture_index: Integer[Array, "vertices"]
    """Texture map index for each vertex."""
    double_sided: Bool[Array, "vertices"]
    """Whether each face is double sided."""

    # Merged maps
    texture_shape: Integer[Array, "objects 2"]
    """Width, height of each texture map."""
    offset: Integer[Array, ""]
    """Width of biggest merged maps, as [0] returned by `merge_maps`."""
    diffuse_map: Texture
    specular_map: SpecularMap

    @staticmethod
    @jaxtyped
    def generate_object_vert_info(
        counts: Sequence[int],
        values: Sequence[Shaped[Array, "..."]],
    ) -> Shaped[Array, "vertices"]:
        """Generate object-wide info for each vertex in merged model as
            vertex-level info.

        Parameters:
          - counts: Number of vertices of each object.
          - values: value to be filled in for each object.

        Returns: Map indices for each face.

        Note: this function cannot be jitted by itself as it uses the value of
            `counts` to create matrices: the shape depends on the value of
            `counts`.
        """
        values: Sequence[Shaped[Array, "_"]] = tree_map(
            lambda count, value: jnp.full(
                (count, *jnp.asarray(value).shape), value),
            counts,
            values,
        )
        map_indices = lax.concatenate(values, dimension=0)

        return map_indices

    @staticmethod
    @jaxtyped
    @jax.jit
    def merge_verts(
        vs: VertsT,
        fs: FaceIndicessT,
    ) -> tuple[VertT, FaceIndicesT]:
        """"""
        counts = [v.shape[0] for v in vs[:-1]]
        cumsum = [0]
        for count in counts:
            cumsum.append(cumsum[-1] + count)

        dtype = jax.dtypes.result_type(*vs)

        # merge vertices
        verts: VertT = lax.concatenate(
            [v.astype(dtype) for v in vs],
            dimension=0,
        )
        # merge faces
        faces: FaceIndicesT = lax.concatenate(
            [f + cumsum[i] for i, f in enumerate(fs)],
            dimension=0,
        )

        return verts, faces

    @staticmethod
    @jaxtyped
    @jax.jit
    def merge_maps(maps: MapsT) -> tuple[MapT, Shape2DT]:
        """Merge maps by concatenating them along the first axis.

        All maps must have the same number of dimensions, i.e., `len(m.shape)`
        must be the same for all maps `m`.

        If the other axises is not the same, they are padded with undefined
        values, keeping [0:shape[i]] as given values, and [shape[i]:] being
        padded values at dimension i. If they are of different dtypes, they are
        promoted together.

        Parameters:
          - maps: a list of maps to merge.

        Returns:
          - A merged map.
          - shape of first and second axis of each map.
        """
        # TODO: find a better way to merge maps
        dims: int = len(maps[0].shape)
        shapes: PyTree[tuple[Integer[Array, ""], ...], ...]
        shapes = tree_map(lambda m: m.shape, maps)
        # pick the largest shape for each dimension
        single_shape: tuple[Integer[Array, ""], ...]
        single_shape = tuple(
            (max((shape[i] for shape in shapes)) for i in range(dims)))

        dtype = jax.dtypes.result_type(*maps)

        new_map = lax.concatenate(
            tree_map(
                lambda m: lax.pad(
                    m,
                    jnp.array(0, dtype=m.dtype),
                    tree_map(
                        lambda capacity, content: (0, capacity - content, 0),
                        single_shape,
                        m.shape,
                    ),
                ).astype(dtype),
                maps,
            ),
            dimension=0,
        )

        return new_map, single_shape[:2]

    @staticmethod
    @jaxtyped
    @jax.jit
    def uv_repeat(
        uv: Float[Array, "2"],
        shape: Integer[Array, "2"],
        map_index: Integer[Array, ""],
        offset: Integer[Array, ""],
    ) -> Float[Array, "2"]:
        """Compute final UV coordinates as if it is repeatedly tiled (in case
            of out-of-bound uv coordinate).

        Parameters:
          - uv: raw uv coordinates, in floating numbers. Only fractional part
            is used, as if the uv coordinates are in [0, 1].
          - shape: of the map being used, according to `map_index`.
          - offset: of each map in the merged maps, as [0] returned by
            `merge_maps`. Only first axis is required, thus here we just need a
            scalar.
          - map_index: index of the map to use.
        """
        assert isinstance(uv, Float[Array, "2"]), f"{uv}"
        assert isinstance(shape, Integer[Array, "2"]), f"{shape}"
        assert isinstance(map_index, Integer[Array, ""]), f"{map_index}"
        assert isinstance(offset, Integer[Array, ""]), f"{offset}"
        # since given uv are in [0, 1] (and may be scaled, if is cube),
        # we need to multiply it by (w, h) of the texture map first.
        # This is equivalent to just obtain the fractional part of uv.
        fractional_uv, _ = jnp.modf(uv)
        fractional_uv = jnp.where(
            fractional_uv < 0,
            fractional_uv + 1,
            fractional_uv,
        )
        assert isinstance(fractional_uv, Float[Array, "2"])

        return (fractional_uv * shape).at[0].add(map_index * offset)


class ModelObject(NamedTuple):
    """Model object with model and transform."""
    model: Model
    """Reference to the model, with mesh, attached maps, etc."""
    local_scaling: Vec3f = jnp.ones(3)
    """Local scaling factors of the object, in x, y, z."""
    transform: ModelMatrix = jnp.identity(4)
    """Transform matrix (model matrix) of the model."""
    # TODO: Support double_sided
    double_sided: Bool[Array, ""] = FALSE_ARRAY
    """Whether the object is double-sided."""


def batch_models(models: Sequence[MergedModel]) -> MergedModel:
    """Merge multiple MergedModel into one, with each field being a batch, with
        batch axis at 0. This is intended to facilitate `jax.vmap`.
    """
    merged_model = MergedModel._make((lax.concatenate(
        [jnp.asarray(model[i])[None, ...] for model in models],
        dimension=0,
    ) for i in range(len(models[0]))))

    return merged_model


@jaxtyped
def merge_objects(objects: Sequence[ModelObject]) -> MergedModel:
    """Merge objects into a single model.

    Parameters:
      - objects: a list of objects to merge.

    Returns: A model containing the merged objects into one single mesh.
    """
    with jax.ensure_compile_time_eval():
        models = [obj.model for obj in objects]

        # broadcasted per vertex info
        counts: list[int] = [len(m.verts) for m in models]

        map_indices: Integer[Array, "vertices"]
        map_indices = MergedModel.generate_object_vert_info(
            counts,
            list(range(len(models))),
        )
        assert isinstance(map_indices, Integer[Array, "vertices"])

        map_wh_per_object = jnp.asarray(
            [m.diffuse_map.shape[:2] for m in models])
        assert isinstance(map_wh_per_object, Integer[Array, "objects 2"])

        double_sided: Bool[Array, "vertices"]
        double_sided = MergedModel.generate_object_vert_info(
            counts,
            [obj.double_sided for obj in objects],
        )
        assert isinstance(double_sided, Bool[Array, "vertices"])

    # merge maps
    diffuse_map, single_map_shape = MergedModel.merge_maps(
        [m.diffuse_map for m in models])
    specular_map, _ = MergedModel.merge_maps([m.specular_map for m in models])

    @jaxtyped
    @partial(jax.jit, inline=True)
    def transform_vert(
        verts: Float[Array, "N 3"],
        local_scaling: Vec3f,
        transform: ModelMatrix,
    ) -> Vertices:
        """Apply transforms defined in `ModelObject` to vertices."""
        world: Float[Array, "N 3"] = Camera.apply_pos(
            verts * local_scaling,
            transform,
        )
        assert isinstance(world, Float[Array, "N 3"])

        return world

    # merge verts
    verts, faces = MergedModel.merge_verts(
        [
            transform_vert(
                verts=obj.model.verts,
                local_scaling=obj.local_scaling,
                transform=obj.transform,
            ) for obj in objects
        ],
        [m.faces for m in models],
    )

    @jaxtyped
    @partial(jax.jit, inline=True)
    def transform_normals(
        normals: Float[Array, "N 3"],
        transform: ModelMatrix,
    ) -> Vertices:
        """Apply transforms defined in `ModelObject` to vertex normals."""
        world: Float[Array, "N 3"] = Camera.apply_vec(
            normals,
            # transform by inverse transpose
            jnp.linalg.inv(transform).T,
        )
        assert isinstance(world, Float[Array, "N 3"])

        return world

    norms, faces_norm = MergedModel.merge_verts(
        [transform_normals(obj.model.norms, obj.transform) for obj in objects],
        [m.faces_norm for m in models],
    )
    uvs, faces_uv = MergedModel.merge_verts(
        [m.uvs for m in models],
        [m.faces_uv for m in models],
    )

    return MergedModel(
        verts=verts,
        norms=norms,
        uvs=uvs,
        faces=faces,
        faces_norm=faces_norm,
        faces_uv=faces_uv,
        texture_shape=map_wh_per_object,
        texture_index=map_indices,
        double_sided=double_sided,
        offset=single_map_shape[0],
        diffuse_map=diffuse_map,
        specular_map=specular_map,
    )
