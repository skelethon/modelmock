
def array_random_split(arr, n, empty_accepted=False):
  ret = []
  arr_len = len(arr)
  first = 0 if empty_accepted else 1
  for i in range(n):
    if i == n-1:
      ret.append(arr)
    else:
      subarr_len = random.randint(first, arr_len - (n - i - 1))
      ret.append(arr[:subarr_len])
      arr = arr[subarr_len:]
      arr_len = len(arr)
  return ret
