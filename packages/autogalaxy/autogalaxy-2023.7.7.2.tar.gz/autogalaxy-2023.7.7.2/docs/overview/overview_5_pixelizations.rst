.. _overview_5_pixelizations:

Non Parametric Models
=====================

Non parametric models use a pixelizations reconstruct a galaxy's light on a pixel-grid.

Unlike ``LightProfile``'s, they are able to reconstruct the light of non-symmetric and irregular galaxies.

We will demonstrate this using a complex galaxy with multiple star forming clumps:

.. image:: https://raw.githubusercontent.com/Jammy2211/PyAutoGalaxy/main/docs/overview/images/pixelizations/image.png
  :width: 400
  :alt: Alternative text

Rectangular Example
-------------------

To fit this image with an ``Inversion``, we first mask the ``Imaging`` object:

.. code-block:: python

   mask = al.Mask2D.circular(
      shape_native=dataset.shape_native, pixel_scales=dataset.pixel_scales, radius=3.0
    )

   dataset = dataset.apply_mask(mask=mask)

To reconstruct the galaxy on a pixel-grid, called a mesh, we simply pass it the ``Mesh`` class we want to reconstruct its
light on.

We also pass a ``Regularization`` scheme which applies a smoothness prior on the source reconstruction.

Below, we use a ``Rectangular`` pixelization with resolution 50 x 50 and a ``Constant`` regularization scheme:

.. code-block:: python

    pixelization = ag.Pixelization(
        mesh=ag.mesh.Rectangular(shape=(50, 50)),
        regularization=ag.reg.Constant(coefficient=1.0),
    )

    galaxy = ag.Galaxy(redshift=1.0, pixelization=pixelization)

Now that our galaxy has a `Pixelization`, we are able to fit the data using it in the
same way as before, by simply passing the galaxy to a `Plane` and using this `Plane` to create a `FitImaging`
object.

.. code-block:: python

    plane = ag.Plane(galaxies=[galaxy])

    fit = ag.FitImaging(dataset=dataset, plane=plane)

Here is what our reconstructed galaxy looks like:

.. image:: https://raw.githubusercontent.com/Jammy2211/PyAutoGalaxy/main/docs/overview/images/pixelizations/rectangular.png
  :width: 400
  :alt: Alternative text

Note how the reconstruction is irregular and has multiple clumps of light, these features would be difficult
to represent using analytic light profiles!

Why Use Pixelizations?
----------------------

From the perspective of a scientific analysis, it may be unclear what the benefits of using an inversion to
reconstruct a complex galaxy are.

When I fit a galaxy with light profiles, I learn about its brightness (`intensity`), size (`effective_radius`),
compactness (`sersic_index`), etc.

What did I learn about the galaxy I reconstructed? Not a lot, perhaps.

Inversions are most useful when combined with light profiles. For the complex galaxy above, we can fit it with light
profiles to quantify the properties of its `bulge` and `disk` components, whilst simultaneously fitting the clumps
with the inversion so as to ensure they do not impact the fit.

The workspace contains examples of how to do this, as well as other uses for pixelizations.

Wrap-Up
-------

This was a brief overview of ``Inverion``'s.

There is a lot more to using ``Inverion``'s then presented here, which is covered in chapters 4 of the **HowToGalaxy**,
specifically:

 - How the inversion's reconstruction determines the flux-values of the galaxy it reconstructs.
 - The Bayesian framework employed to choose the appropriate level of `Regularization` and avoid overfitting noise.
 - Unphysical model solutions that often arise when using an `Inversion`.