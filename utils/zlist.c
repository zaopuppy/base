#include "zlist.h"

#include <stdlib.h>
#include <assert.h>

// impliment
struct list_t*
list_new() {
	struct list_t *list = (struct list_t*)malloc(sizeof(struct list_t));

	list->size = 0;
	list->first = NULL;
	list->last = NULL;

	return list;
}

void
list_free(struct list_t *list) {
	struct node_t *nd;
	struct node_t *tmp;

	nd = list->first;
	while (nd) {
		tmp = nd;
		nd = nd->next;
		free(tmp);
	}

	free(list);
}

// TODO: rewrite it with macro
void
list_push_front(struct list_t *list, struct node_t *new_nd) {
	struct node_t *first = list->first;

	if (!first) {
		assert(list->size == 0);
		list->first = new_nd;
		list->last = new_nd;
		new_nd->next = NULL;
		new_nd->prev = NULL;
		new_nd->list = list;

		list->size = 1;
		
		return;
	}

	struct node_t *next = first->next;
	if (next) {
		first->next->prev = new_nd;
		first->next = new_nd;
		new_nd->next = next;
		new_nd->prev = first;
	} else {
		first->next = new_nd;
		new_nd->next = NULL;
		new_nd->prev = first;
	}

	++(list->size);
}

void
list_sort_push(struct list_t *list, struct node_t *new_nd, comparator cmp) {
	struct node_t *nd;
	int rv;

	if (list->first == NULL) {
		return list_push_front(list, new_nd);
	}
	
	for (nd = list->first; nd; nd = nd->next) {
		rv = cmp(new_nd, nd);
		if (rv < 0) {
			return list_insert(list, nd, new_nd);
		}

		// last one
		if (nd->next == NULL) {
			return list_append(list, nd, new_nd);
		}
	}

	// should not happen
	assert(0);
}

void
list_insert(struct list_t *list, struct node_t *nd, struct node_t *new_nd) {
	struct node_t* prev = nd->next;
	if (prev) {
		nd->prev->next = new_nd;
		nd->prev = new_nd;
		new_nd->next = nd;
		new_nd->prev = prev;
	} else { // new header
		nd->prev = new_nd;
		new_nd->prev = NULL;
		new_nd->next = nd;
		// update `first'
		list->first = new_nd;
	}

	++(list->size);
}

void
list_append(struct list_t *list, struct node_t *nd, struct node_t *new_nd) {
	
	struct node_t* next = nd->next;
	if (next) {
		nd->next->prev = new_nd;
		nd->next = new_nd;
		new_nd->next = next;
		new_nd->prev = nd;
	} else {
		nd->next = new_nd;
		new_nd->prev = nd;
		new_nd->next = NULL;
		// update `last'
		list->last = new_nd;
	}

	++(list->size);
}

void
list_remove(struct list_t *list, struct node_t *nd)
{
	// should not be head
	assert(nd);

	struct node_t *prev, *next;
	
	prev = nd->prev;
	next = nd->next;

	if (prev) {
		prev->next = next;
	} else {
		// update `first'
		list->first = nd->next;
	}
	if (next) {
		next->prev = prev;
	} else {
		// update `last'
		list->last = nd->prev;
	}

	nd->prev = NULL;
	nd->next = NULL;

	free(nd);

	--(list->size);
}


