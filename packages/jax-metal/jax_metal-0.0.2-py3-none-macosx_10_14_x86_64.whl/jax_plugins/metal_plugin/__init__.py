from pathlib import Path
import platform

import jax._src.xla_bridge as xb

def initialize():
  v, _, _ = platform.mac_ver()
  base_version = v.split('.')[0]
  if (int(base_version) > 13):
      platform_lib_name = "pjrt_plugin_metal_14.dylib"
  else:
      platform_lib_name = "pjrt_plugin_metal_13.dylib"

  path = Path(__file__).resolve().parent / platform_lib_name
  xb.register_plugin("METAL",
                     priority=500,
                     library_path=str(path),
                    )
