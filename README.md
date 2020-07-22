# k8s-split-manifest

# Purpose

Split out aggregated YAML to individual files.

Where the manifest has single objects a 'kind', the object will be written into the current directory as name: 'kind'.yaml

Where the manifest has multiple object of a 'kind', the objects will be written into a subdirectory of name 'kind' as 'metadata.name'.yaml

The script is meant to extract individual objects from YAML files containing multiple objects. (Seperated by '---')

# Notes

This is beta software and may not be fit for your own use.

This is different from the k8s-backup-dump script (which handles objects in a YAML list), this script handles objects seperated by '---'.

# Usage

```
./k8s-split-manifest.py manifest.yaml
```

# License

```
k8s-split-manifest for splitting out aggregated YAML to individual files.
Copyright (C) 2020    Brian Czapiga

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See <http://www.gnu.org/licenses/> for more information.
```
