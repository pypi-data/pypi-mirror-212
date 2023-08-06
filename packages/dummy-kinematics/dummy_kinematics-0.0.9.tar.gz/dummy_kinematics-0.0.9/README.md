# dummy_kinematics

[![PyPI - Version](https://img.shields.io/pypi/v/dummy-kinematics.svg)](https://pypi.org/project/dummy-kinematics)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dummy-kinematics.svg)](https://pypi.org/project/dummy-kinematics)

-----

**Description**

- This is a pkg for dummy-kinematics analysis

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install dummy-kinematics
```
## Example usage

```console
from dummy_kinematics.ppt_factory import H3_05_PPT_Factory,THOR_PPT_Factory
# for simplified example, Assumption MPDB is DR 11 Thor, 13 and 14 is H3_05

# data source is the csv or xlsx file path
pt = r"E:\workat\official CNCAP\odata\MPDB\pt_mpdb.csv"
fvc = r"E:\workat\official CNCAP\odata\MPDB\corrected_fvc_mpdb.xlsx"

factory = (THOR_PPT_Factory().
        add_a_data_coverter(name="PT",
                        path=pt,
                        speed_kph=50.80,
                        x_code="17CPILLELO02ACXD", # setting body wave isocode
                        y_code="17CPILLELO02ACYD",
                        z_code="17CPILLELO02ACZD").
        add_a_data_coverter(name="FVC", path=fvc,
                        speed_kph=49.9,
                        x_code="14SILBBCPIL0ACXD",
                        y_code="14SILBBCPIL0ACYD",
                        z_code="14SILBBCPIL0ACZD").
        body_performance_report().
        set_current_dummy("11", "THOR").
        create_full_prs("DR dummy report")
        )

factory = (H3_05_PPT_Factory().
        from_other_factory(factory).
        set_current_dummy("13","H3_05").
        create_full_prs("PS dummy report").
        set_current_dummy("14","H3_05").
        create_full_prs("RL dummy report")
        )

factory.save_ppt_report("MPDB_20221228.pptx")

```

## License

`dummy-kinematics` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
