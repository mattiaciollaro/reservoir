# reservoir

Just an implementation of [reservoir sampling](https://en.wikipedia.org/wiki/Reservoir_sampling)!

## Depends on

- `numpy`

## Usage

Instantiate a reservoir with

```python
from reservoir import Reservoir

reservoir = Reservoir(size=10)
```

You can specify the desired sample size with the `size` parameter.
Note that `size` must be a positive integer.

### Sampling

The `Reservoir` class implements the `sample` method, which is used to sample
`size` items from an *iterable* of arbitrary/unknown length (typically, a
Python generator).

```python
# simulate a stream
stream_one = (n for n in range(1000000))
```

The sampling is performed with

```python
reservoir.sample(gen=stream_one, seed=0)
```

where `gen` is the iterable from which to sample `size` items and `seed` is an
integer used to seed the random number generator.

The resulting sample can be accessed via the `samples` attribute.

```python
print(reservoir.samples)
```

```text
[73023, 266953, 460324, 831588, 126670, 868561, 345397, 661481, 996190, 670678]
```

So far, the sampler has seen

```python
print(reservoir.seen)
```

```text
1000000
```

items.

If more data is flowing in, you can easily resume the sampling process:

```python
# simulate another stream
stream_two = (n for n in range(1000000, 1500000))

# resume the sampling
reservoir.sample(gen=stream_two)

# sample after the second stream
print(reservoir.samples)
```

```text
[1333461, 266953, 460324, 1238853, 126670, 868561, 345397, 661481, 996190, 670678]
```

At this point, the sampler has seen

```python
print(reservoir.seen)
```

```text
1500000
```

items.

### Resetting

You can reset the sampler with

```python
reservoir.reset()
```

Now the sample is empty

```python
print(reservoir.samples)
```

```text
[]
```

and the sampler has seen

```python
print(reservoir.seen)
```

```text
0
```

items.

However, the `size` attribute is untouched:

```python
print(reservoir.size)
```

```text
10
```
