# GenColorPickerTableCells.py

Generate color picker table cells for Qt5's table widget.

## Getting Started

### Prerequisites

Install build environment. I use Ninja to reduce project build time.

```shell
sudo apt-get -y install build-essential cmake git ninja-build
```

Then install dependencies for the project.

```shell
sudo apt-get -y install qt5-default oce-draw liboce-\*-dev libeigen3-dev libtbb-dev zlib1g-dev
```

## Running
> Note: Python version >=3.7.0 is required.

With Python 3

```shell
python GenColorPickerTableCells.py
```

Create a build directory.

```shell
cd oce-jt
mkdir build
```

Configure and build the project with Ninja.

```shell
cd build
cmake -G "Ninja" ..
ninja
```

Finally, the JT Assistant application can be run with the following command:

```shell
./JTAssistant/JTAssistant
```

## License

This project is licensed under the GNU General Public License v2.0 - see the [LICENSE.txt](LICENSE.txt) file for details.