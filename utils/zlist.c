#include "zlist.h"


#include <stdlib.h>


// impliment
struct node_t*
new_list() {
	struct node_t *head = (struct node_t*)malloc(sizeof(struct node_t));

	head->prev = NULL;
	head->next = NULL;

	return head;
}

// TODO: rewrite it with macro
struct node_t*
push_front(struct node_t *head, struct node_t *new_nd) {
	struct node_t *next = head->next;

	if (next) {
		head->next->prev = new_nd;
		head->next = new_nd;
		new_nd->next = next;
		new_nd->prev = head;
	} else {
		head->next = new_nd;
		new_nd->next = NULL;
		new_nd->prev = head;
	}

	return new_nd;
}

struct node_t*
sort_push(struct node_t *head, struct node_t *new_nd, comparator cmp) {
	struct node_t *nd;
	int rv;

	if (head->next == NULL) {
		return push_front(head, new_nd);
	}
	
	for (nd = head->next; nd; nd = nd->next) {
		rv = cmp(new_nd, nd);
		if (rv < 0) {
			return insert(nd, new_nd);
		}

		// last one
		if (nd->next == NULL) {
			return append(nd, new_nd);
		}
	}

	// should not happen
	return NULL;
}

struct node_t*
insert(struct node_t *nd, struct node_t *new_nd) {
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
	}

	return new_nd;
}

struct node_t*
append(struct node_t *nd, struct node_t *new_nd) {
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
	}

	return new_nd;
}

