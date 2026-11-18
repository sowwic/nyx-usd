nyx-usd
=======

v1.0.0
------
* (#1) Add USD nodes for Nyx that run in an interpreter with ``pxr`` through the bridge, so Nyx never imports USD
* (#1) Add ``nyx_usd.ops``, the USD operations the nodes call: plain functions over JSON values, with stages kept open in the client and passed between nodes as handles.
* (#1) Add nodes for stages (open, create, save, close), prims (add, remove, find, query, rename, move, copy, active, kind, metadata) and attributes (set and get, at a time, time samples, list, remove).
* (#1) Add nodes for stage settings (metadata, time range, fps, up axis, meters per unit, default prim, stage info).
* (#1) Add nodes for composition: references, payloads, inherits, sublayers, variant sets, export to string and flatten.
* (#1) Add nodes for transforms, bounds, visibility, purpose, cubes, spheres, meshes and materials.
* (#1) Add the ``USD Client`` node, a Launch Process node that starts the client in the interpreter given by ``python`` or ``NYX_USD_PYTHON``.
* (#1) Tag the nodes by area (``tags:prim``, ``tags:composition``, ...) so the palette can filter them.
* (#1) Add the user and developer documentation.
