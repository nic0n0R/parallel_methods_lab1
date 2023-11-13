import concurrent.futures
import os
import threading
import sys

tasks_counter = 0
variable_lock = threading.Lock()


def copy_file(src_path, dst_path):
    with open(src_path, 'rb') as src_file:
        with open(dst_path, 'wb') as dst_file:
            while True:
                data = src_file.read(4096)
                if not data:
                    break
                dst_file.write(data)
    global tasks_counter
    with variable_lock:
        tasks_counter -= 1


def recoursive_copy(src_dir, dst_dir, executor):
    global tasks_counter
    new_dir_name = os.path.join(dst_dir, os.path.basename(src_dir))
    os.makedirs(new_dir_name, exist_ok=True)

    for file_name in os.listdir(src_dir):
        full_filename = os.path.join(src_dir, file_name)
        if os.path.isfile(full_filename):
            new_file_name = os.path.join(new_dir_name, file_name)
            executor.submit(copy_file, full_filename, new_file_name)
            with variable_lock:
                tasks_counter += 1
            # copy_file(full_filename, new_file_name)
        elif os.path.isdir(full_filename):
            executor.submit(recoursive_copy, full_filename, new_dir_name, executor)
            with variable_lock:
                tasks_counter += 1
            # recoursive_copy(full_filename, new_dir_name, executor)

    with variable_lock:
        tasks_counter -= 1


def main():
    if len(sys.argv) != 4:
        print("Использование: py 12.py <\"src_dir\"> <\"dst_dir\"> <num_threads>")
        sys.exit(1)

    src_dir = sys.argv[1]
    dst_dir = sys.argv[2]
    threads_amount = int(sys.argv[3])
    # src_dir = r"D:\6_course\1_semestr\параллельные методы и алгоритмы Максименко\лаба1\laba1_proj\task12_src"
    # dst_dir = r"D:\6_course\1_semestr\параллельные методы и алгоритмы Максименко\лаба1\laba1_proj\task12_dst"
    # threads_amount = 2

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads_amount) as executor:
        recoursive_copy(src_dir, dst_dir, executor)

        global tasks_counter
        tasks_counter += 1
        while tasks_counter != 0:
            pass

    print("Копирование завершено.")


if __name__ == '__main__':
    main()
    #  py 12.py "D:\6_course\1_semestr\параллельные методы и алгоритмы Максименко\лаба1\laba1_proj\task12_src" "D:\6_course\1_semestr\параллельные методы и алгоритмы Максименко\лаба1\laba1_proj\task12_dst" 2