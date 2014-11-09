
void bubble_sort(int *data, int data_len)
{
  int tmp;
  for (int i = 0; i < data_len - 1; ++i) {
    for (int j = 0; j < data_len - i; ++j) {
      if (data[j] > data[j+1]) {
        tmp = data[j+1];
        data[j+1] = data[j];
        data[j] = tmp;
      }
    }
  }
}

void quick_sort(int *data, int data_len)
{
  int tmp;
  if (data_len <= 1) {
    return;
  } else if (data_len == 2) {
    if (data[1] < data[0]) {
      tmp = data[1];
      data[1] = data[0];
      data[0] = tmp;
    }
    return;
  }

  // data[0] is pivot
  int i, j;
  for (i = 1, j = data_len-1; i <= j;) {
    if (data[i] > data[0]) {
      tmp = data[j];
      data[j] = data[i];
      data[i] = tmp;
      --j;
    }
    ++i;
  }

  printf("i=%d, j=%d\n", i, j);

  quick_sort(data, i);
  if (data_len - i > 0) {
    quick_sort(data+i, data_len - i);
  }
}

