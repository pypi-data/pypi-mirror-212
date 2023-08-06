# Copyright 2023 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

"""Acquisition functions and builders implementations."""

from typing import Optional

import jax
from jax import numpy as jnp
from tensorflow_probability.substrates import jax as tfp
from vizier._src.algorithms.designers.gp import acquisitions as acquisitions_lib
from vizier._src.jax import stochastic_process_model as sp
from vizier._src.jax import types


tfd = tfp.distributions
tfp_bo = tfp.experimental.bayesopt
tfpke = tfp.experimental.psd_kernels


def _build_predictive_distribution(
    xs: types.Features,
    model: sp.StochasticProcessModel,
    state: types.GPState,
    use_vmap: bool = True,
) -> tfd.Distribution:
  """Generates the predictive distribution on array function."""

  def _predict_on_array_one_model(
      model_state: types.ModelState, *, xs: types.Features
  ) -> tfd.Distribution:
    return model.apply(
        model_state,
        xs,
        state.data.features,
        state.data.labels,
        method=model.posterior_predictive,
        observations_is_missing=state.data.label_is_missing,
    )

  if not use_vmap:
    return _predict_on_array_one_model(state.model_state, xs=xs)

  def _predict_mean_and_stddev(state_: types.ModelState) -> tfd.Distribution:
    dist = _predict_on_array_one_model(state_, xs=xs)
    return {'mean': dist.mean(), 'stddev': dist.stddev()}  # pytype: disable=attribute-error  # numpy-scalars

  # Returns a dictionary with mean and stddev, of shape [M, N].
  # M is the size of the parameter ensemble and N is the number of points.
  pp = jax.vmap(_predict_mean_and_stddev)(state.model_state)
  batched_normal = tfd.Normal(pp['mean'].T, pp['stddev'].T)  # pytype: disable=attribute-error  # numpy-scalars

  return tfd.MixtureSameFamily(
      tfd.Categorical(logits=jnp.ones(batched_normal.batch_shape[1])),
      batched_normal,
  )


def predict_on_array(
    xs: types.Features,
    model: sp.StochasticProcessModel,
    state: types.GPState,
    use_vmap: bool = True,
):
  """Prediction function on features array."""
  dist = _build_predictive_distribution(xs, model, state, use_vmap)
  return {'mean': dist.mean(), 'stddev': dist.stddev()}


def sample_on_array(
    xs: types.Features,
    num_samples: int,
    key: jax.random.KeyArray,
    model: sp.StochasticProcessModel[types.Features],
    state: types.GPState,
    use_vmap: bool = True,
):
  """Sample the underlying model on features array."""
  dist = _build_predictive_distribution(xs, model, state, use_vmap)
  return dist.sample(num_samples, seed=key)


def acquisition_on_array(
    xs: types.Features,
    model: sp.StochasticProcessModel,
    acquisition_fn: acquisitions_lib.AcquisitionFunction,
    state: types.GPState,
    trust_region: Optional[acquisitions_lib.TrustRegion] = None,
    use_vmap: bool = True,
):
  """Acquisition function on features array."""
  dist = _build_predictive_distribution(xs, model, state, use_vmap)
  acquisition = acquisition_fn(dist, state.data.features, state.data.labels)
  if trust_region is not None:
    distance = trust_region.min_linf_distance(xs)
    # Due to output normalization, acquisition can't be nearly as
    # low as -1e12.
    # We use a bad value that decreases in the distance to trust region
    # so that acquisition optimizer can follow the gradient and escape
    # untrusted regions.
    return jnp.where(
        ((distance <= trust_region.trust_radius) &
         (trust_region.trust_radius < 0.5)),
        acquisition,
        -1e12 - distance
    )
  else:
    return acquisition


def multi_acquisition_on_array(
    xs: types.Features,
    model: sp.StochasticProcessModel,
    acquisition_fns: dict[str, acquisitions_lib.AcquisitionFunction],
    state: types.GPState,
    trust_region: Optional[acquisitions_lib.TrustRegion] = None,
    use_vmap: bool = True,
):
  """Evaluates multiple acquisition functions on a features array."""
  dist = _build_predictive_distribution(xs, model, state, use_vmap)
  acquisitions = []
  for acquisition_fn in acquisition_fns.values():
    acquisitions.append(
        acquisition_fn(dist, state.data.features, state.data.labels))
  acquisition = jnp.stack(acquisitions, axis=0)

  if trust_region and trust_region.trust_radius < 0.5:
    distance = trust_region.min_linf_distance(xs)
    # Due to output normalization, acquisition can't be nearly as
    # low as -1e12.
    # We use a bad value that decreases in the distance to trust region
    # so that acquisition optimizer can follow the gradient and escape
    # untrusted regions.
    return jnp.where(
        distance <= trust_region.trust_radius,
        acquisition,
        -1e12 - distance,
    )
  else:
    return acquisition
