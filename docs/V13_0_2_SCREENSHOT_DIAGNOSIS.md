# v13.0.2 Screenshot Diagnosis

The Android screenshot showed three coupled symptoms: the regional map was visible through the supposed paper interiors; text and icons inside the same elements were faded; and the title/action-card geometry appeared clipped.

Root cause: v13.0.1 applied CSS `mask-image` directly to container elements. CSS masks affect the composited element including descendants, so the mask altered the opacity of text/icons/controls as well as the paper background. The standalone SVG paper artwork already has torn transparent edges and therefore does not need a parent CSS mask.

Repair: remove parent masks, render the SVG paper art only as the background image, force normal opacity/blending on functional content, keep the map in a lower stacking context, and bump the service-worker cache.
