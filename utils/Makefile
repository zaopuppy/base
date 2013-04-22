AR     := ar
CC     := gcc
CXX    := g++
CPP    := gcc
LEX    := flex
YACC   := bison

TARGET := libzutil.a
CFILES := zlist.c zlog.c
CXXFILES :=

# intermedia files
OBJFILES := $(CFILES:%.c=obj/%.o) $(CXXFILES:%.cc=obj/%.o)
DEPFILES := $(OBJFILES:%.o=%.d)

CFLAGS := -Wall -g
LDFLAGS :=
ARFLAGS := -r

$(TARGET) : $(OBJFILES)
	rm -f $@
	$(AR) $(ARFLAGS) $@ $(OBJFILES)

obj/%.d : %.cc
	rm -f $@
	$(CXX) $(CFLAGS) -MT $(@:%.d=%.o) -MM -o $@ $<

obj/%.d : %.c
	rm -f $@
	$(CC) $(CFLAGS) -MT $(@:%.d=%.o) -MM -o $@ $<

obj/%.o : %.cc
	rm -f $@
	$(CXX) $(CFLAGS) -c -o $@ $<

obj/%.o : %.c
	rm -f $@
	$(CC) $(CFLAGS) -c -o $@ $<

include $(DEPFILES)

.PHONY : clean rebuild test gdb

check :
	if [ ! -d obj ]; then rm -rf obj; mkdir obj; fi

clean :
	rm -f $(OBJFILES) $(DEPFILES)

rebuild : clean $(TARGET)

test : $(TARGET)
	@clear
	@./$(TARGET)



