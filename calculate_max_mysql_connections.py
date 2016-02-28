###
# This is sloppy, update this to take arguments or read directly from the mysql database.
# Also, add more variables, which can be found at:
# http://www.mysqlcalculator.com/
###

total_RAM = 17179869184.0

global_buffers = {
    "key_buffer_size": 235929600,
    "innodb_buffer_pool_size":  157286400,
    "innodb_log_buffer_size": 1048576,
    "innodb_additional_mem_pool_size": 1048576,
    "query_cache_size": 33554432
}

thread_buffers = {
    "sort_buffer_size": 2097144,
    "myisam_sort_buffer_size": 8388608,
    "read_buffer_size":  131072,
    "join_buffer_size":  131072,
    "read_rnd_buffer_size": 2097152,
    "thread_stack": 262144
}

global_total = 0.0
thread_total = 0.0

for x, y in global_buffers.items():
    global_total += y

for x, y in thread_buffers.items():
    thread_total += y

max_connect = (total_RAM - global_total) / thread_total

print("Global thread total : {}".format(global_total))
print("Thread thread total : {}".format(thread_total))
print("Max connections : {}".format(max_connect))
