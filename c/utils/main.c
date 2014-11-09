#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <assert.h>

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

void print_list(struct list_t *list)
{
	struct node_t *nd;
	struct Data* data;
	int i;

	printf("size of list: %u\n", list->size);

	i = 0;
	for (nd = list->first; nd; nd = nd->next) {
		data = GET_DATA(nd, struct Data, node);
		printf("%d: %d\n", i, data->i);
		++i;
	}
}

void reverse_print_list(struct list_t *list)
{
	struct node_t *nd;
	struct Data* data;
	int i;

	printf("size of list: %u\n", list->size);

	i = 0;
	for (nd = list->last; nd; nd = nd->prev) {
		data = GET_DATA(nd, struct Data, node);
		printf("%d: %d\n", i, data->i);
		++i;
	}
}

int test_list()
{
	struct list_t *list = list_new();
	
	struct Data *data;

	int i;
	for (i = 0; i < 10; ++i) {
		data = (struct Data*)malloc(sizeof(struct Data));
		data->i = i;
		list_sort_push(list, &data->node, data_comparator);
	}

	print_list(list);
	reverse_print_list(list);


	struct node_t *nd;
	for (nd = list->first; nd; nd = nd->next) {
		data = GET_DATA(nd, struct Data, node);
		if (data->i == 4) {
			list_remove(list, nd);
			break;
		}
	}
	
	print_list(list);
	reverse_print_list(list);

	list_free(list);

	return 0;
}

// -----------------------------------
// node-id: 0~65535 (uint16_t)
// server-id: uint32_t
struct list_t *g_node_list;
struct list_t *g_server_list;

const uint16_t MAX_NODE_NUM = 0xFFFF;
uint16_t g_delta = 0xFFFF;

int get_node_id()
{
	return 0;
}

// 
// return node id
int add_node()
{
	// calculate node-id first
	// delta = MAX_NODE_NUM/node_num;
	// node-id = n * delta
	return 0;
}

int main(int argc, char* argv[])
{
	g_node_list = list_new();
	g_server_list = list_new();

	assert(g_node_list);
	assert(g_server_list);

	return 0;
}



