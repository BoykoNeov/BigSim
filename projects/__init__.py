"""BigSim simulators (ARCHITECTURE.md build order: Steel → Microchip → Planet).

Each project recomposes the frozen shared engines (``engines/``) into a domain
simulator. The first and engine-defining one is ``projects.steel`` — it builds &
freezes the diffusion/heat spine the other two inherit.
"""
