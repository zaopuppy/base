#include <stdio.h>

#include "sort.h"

void print(int *data, int data_len)
{
  for (int i = 0; i < data_len; ++i) {
    printf("%d\t", data[i]);
  }
  printf("\n");
}

int main(int argc, char *argv[])
{
  int data[] = { 5, 4, 3, 2, 1 };
  print(data, sizeof(data)/sizeof(int));
  // bubble_sort(data, sizeof(data)/sizeof(int));
  quick_sort(data, sizeof(data)/sizeof(int));
  print(data, sizeof(data)/sizeof(int));
  return 0;
}

