# DataCapturer

DataCapturer allows the user to store a list of integers and determine the total count of stored integers above, below, or in between provided values.

## Detailed Description

The `data_capture` script contains two classes and a helper function for data validation.

A `DataCapture` instance accepts individual integers passed to its `add` method. It only accepts values under 1000. If the same value is added multiple times, that counts as multiple values.

When the instance's `build_stats` method is called, it returns a `Stats` instance with the stored values for counting.

`Stats` has three methods.

`less` and `greater` take one integer each and return a count of the number of lesser or greater values respectively.

`between` takes two integers. It returns the total count of values between the two integers, inclusive.

I attempted to optimize the performance of each method. `less`, `greater` and `between` run in O(1) time. I still think there should be a way to squeeze more out of `build_stats`. See the note in its docstring.

## Running DataCapturer

Since I've only used the standard library, there is no need to set up a virtual environment. You will need to be running at least python 3.6 as I'm using f-strings.

1. Clone the repo.
2. `cd` into the `datacapturer` folder.
3. Open the Python interpreter by typing `python` (or specify the version if needed e.g. `python3.6`)
4. `from data_capture import DataCapture`.
5. `capture = DataCapture()`.
6. `capture.add(<int>)` to add `<int>` to your data.
7. Once you are satisfied with your data, `stats = capture.build_stats()`.
8. Now you can call `stats.less` or `stats.greater` with a single integer, or `stats.between` with two integers, as described in the detailed description above.
9. To run tests, call `python test_data_capture.py` from the `datacapturer` folder.
