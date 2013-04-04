#ifndef _Z_LIST_H__
#define _Z_LIST_H__

struct node_t;

struct list_t {
	unsigned int size;
	struct node_t *first;
	struct node_t *last;
};

struct node_t {
	struct node_t *prev;
	struct node_t *next;
	struct list_t *list;
};


// declare
// return minus number if the second is smaller than the first one.
typedef int (*comparator)(struct node_t *, struct node_t *);

struct list_t* list_new();
void list_free(struct list_t *list);
void list_push_front(struct list_t *list, struct node_t *new_nd);
void list_sort_push(struct list_t *list, struct node_t *new_nd, comparator cmp);
void list_insert(struct list_t *list, struct node_t *nd, struct node_t *new_nd);
void list_append(struct list_t *list, struct node_t *nd, struct node_t *new_nd);
void list_remove(struct list_t *list, struct node_t *nd);

#define GET_DATA(ptr_, data_type_, member_)															\
	(data_type_*)((char*)ptr_ - (unsigned long)&( ((data_type_*)0)->member_ ))


#endif // _Z_LIST_H__

