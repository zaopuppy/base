#ifndef _Z_LIST_H__
#define _Z_LIST_H__

struct node_t {
	struct node_t *prev;
	struct node_t *next;
};


// declare
// return minus number if the second is smaller than the first one.
typedef int (*comparator)(struct node_t *, struct node_t *);

struct node_t* new_list();
struct node_t* push_front(struct node_t *head, struct node_t *new_nd);
struct node_t* sort_push(struct node_t *head, struct node_t *new_nd, comparator cmp);
struct node_t* insert(struct node_t *nd, struct node_t *new_nd);
struct node_t* append(struct node_t *nd, struct node_t *new_nd);

#define GET_DATA(ptr_, data_type_, member_)															\
	(data_type_*)((char*)ptr_ - (unsigned long)&( ((data_type_*)0)->member_ ))


#endif // _Z_LIST_H__

