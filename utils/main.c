#include <stdio.h>
#include <stdlib.h>

#include "zlist.h"

struct Data {
	struct node_t node;
	int i;
};

// < 0: less than
// = 0: equal
// > 0: gainter than
int data_comparator(struct node_t *n1, struct node_t *n2) {
	struct Data *d1, *d2;

	d1 = GET_DATA(n1, struct Data, node);
	d2 = GET_DATA(n2, struct Data, node);

	return (d1->i - d2->i);
}

void print_list(struct node_t *list)
{
	struct node_t *nd;
	struct Data* data;

	int i = 0;
	for (nd = list->next; nd; nd = nd->next) {
		data = GET_DATA(nd, struct Data, node);
		printf("%d: %d\n", i, data->i);
		++i;
	}
}

int main(int argc, char* argv[])
{
	struct node_t *list = new_list();
	struct node_t *last;
	
	struct Data *data;

	int i;
	for (i = 0; i < 10; ++i) {
		data = (struct Data*)malloc(sizeof(struct Data));
		data->i = i;
		// last = push_front(list, &data->node_);
		last = sort_push(list, &data->node, data_comparator);
	}

	print_list(list);

	return 0;
}




