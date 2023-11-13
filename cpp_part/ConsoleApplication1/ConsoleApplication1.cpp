#include <iostream>
#include <omp.h>
#include <random>
#include <chrono>

using std::cout;
using std::endl;

int partition(int arr[], int l, int r){
            int i = l + 1;
            int j = r;
            int key = arr[l];
            int temp;
            while(true){
                while(i < r && key >= arr[i])
                    i++;
                while(key < arr[j])
                    j--;
                if(i < j){
                    temp = arr[i];
                    arr[i] = arr[j];
                    arr[j] = temp;
                }else{
                    temp = arr[l];
                    arr[l] = arr[j];
                    arr[j] = temp;
                    return j;
                }
            }
        }

void quickSort(int arr[], int l, int r, int& k){
            if(l < r){
                int p = partition(arr, l, r);
                //cout << "pivot " << p << " found by thread no. " << k << endl; 
				omp_set_num_threads(8);
                #pragma omp parallel sections
                {
                    #pragma omp section
                    {
                        //k = k + 1;
                        //cout << endl << "Thread no. " << omp_get_thread_num() << endl;
                        quickSort(arr, l, p-1, k);
                        
                    }
                    #pragma omp section
                    {
                        //k = k + 1;
						//cout << endl << "Thread no. " << omp_get_thread_num() << endl;
                        quickSort(arr, p+1, r, k);
                    }
                }
            }
        }


// task 4
void task1() {
    int arr[100];
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 100);

    for (int i = 0; i < 100; i++) {
        arr[i] = dis(gen);
    }
    int n = sizeof(arr) / sizeof(arr[0]);

    std::cout << "Fast sort using OpenMP" << std::endl << std::endl;

    std::cout << "Arr before sort: ";
    for (int i = 0; i < 100; i++) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl << std::endl << std::endl;

    // замеряем время выполнения функции
    auto start = std::chrono::high_resolution_clock::now();
    int k = 0;
    omp_set_nested(1);
    omp_set_dynamic(true);
    // Сортируем массив
    quickSort(arr, 0, n - 1, k);
    auto end = std::chrono::high_resolution_clock::now();

    auto duration = end - start;


    // Выводим отсортированный массив
    std::cout << "Sorted arr: ";
    for (int i = 0; i < n; i++) {
        std::cout << arr[i] << " ";
	}
    std::cout << std::endl;

    // кастуем время работы функции из микро-секунд в мили-секунды
    std::chrono::microseconds microseconds(duration.count());
    std::chrono::milliseconds seconds = std::chrono::duration_cast<std::chrono::milliseconds>(microseconds);

    std::cout << "Func time: " << seconds.count() << " milisecs" << std::endl;
}


void merge(int* arr, int left, int mid, int right) {
    int* low = new int[mid - left + 1];
    int* high = new int[right - mid];

    for (int i = left; i <= mid; i++) {
        low[i - left] = arr[i];
    }
    for (int i = mid + 1; i <= right; i++) {
        high[i - mid - 1] = arr[i];
    }

    // слияние дух временных массивов в один
    int i = 0, j = 0, k = left;
    while (i < mid - left + 1 && j < right - mid) {
        if (low[i] <= high[j]) {
            arr[k++] = low[i++];
        }
        else {
            arr[k++] = high[j++];
        }
    }

    // копируем оставшиесся элементы из первовго списка
    while (i < mid - left + 1) {
        arr[k++] = low[i++];
    }

    // копируем оставшиесся элементы из первовго списка
    while (j < right - mid) {
        arr[k++] = high[j++];
    }

    // освобождаем память
    delete[] low, high;
}

void merge_sort(int* arr, int low, int high) {
    if (low >= high) return;

    int mid = low + (high - low) / 2;
	omp_set_num_threads(4);
    #pragma omp parallel sections
    {
        #pragma omp section
        {
            merge_sort(arr, low, mid);
        }
        #pragma omp section
        {
            merge_sort(arr, mid + 1, high);
        }
    }

    // Сливаем две отсортированные части
    merge(arr, low, mid, high);
}

// task 6
void task2() {

    std::cout << std::endl << std::endl << "Merge sorting using OpenMP" << std::endl << std::endl;

    int arr[100000];
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 100);

    for (int i = 0; i < 100; i++) {
        arr[i] = dis(gen);
    }
    int n = sizeof(arr) / sizeof(arr[0]);

    std::cout << "Arr before sort: ";
    for (int i = 0; i < 100; i++) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl << std::endl << std::endl;


    // замеряем время выполнения функции
    auto start = std::chrono::high_resolution_clock::now();
    
    // Сортируем массив
    merge_sort(arr, 0, n - 1);
    
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = end - start;


    // Выводим отсортированный массив
    std::cout << "Sorted arr: ";
    for (int i = 0; i < n; i++) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;

    // кастуем время работы функции из микро-секунд в мили-секунды
    std::chrono::microseconds microseconds(duration.count());
    std::chrono::milliseconds seconds = std::chrono::duration_cast<std::chrono::milliseconds>(microseconds);

    std::cout << "Func time: " << seconds.count() << " milisecs" << std::endl;
}


double pi_monte_carlo(int n) {
    // Создаём генератор случайных чисел
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(0.0, 1.0);

    // Считаем количество точек, попавших в круг
    int in_circle = 0;
    omp_set_num_threads(4);
    #pragma omp parallel for reduction(+:in_circle)
	    for (int i = 0; i < n; i++) {
	    	//std::cout << std::endl << "Amount of the threads: " << omp_get_num_threads();
	    	//printf("num of available procs = %d\n", omp_get_num_procs());
			//printf("is in parallel tread : %d\n", omp_in_parallel());
			//printf("current thread = %d\n", omp_get_thread_num());
        	double x = dis(gen);
        	double y = dis(gen);

        	// Если точка попала в круг, то увеличиваем счётчик
        	if (x * x + y * y <= 1.0) {
            	in_circle++;
        	}
    	}

    // Вычисляем значение числа π
    return 4.0 * in_circle / n;
}


// task 8
void task3() {
    // Количество точек
    int n = 1000000;
    double pi = 0.0;
    // Запускаем параллельное вычисление
    auto start = std::chrono::high_resolution_clock::now();

    pi = pi_monte_carlo(n / omp_get_num_threads());
 


    auto end = std::chrono::high_resolution_clock::now();
    auto duration = end - start;


    // Выводим результат
    std::cout << std::endl << "Found num Pi by Monte-Carlo method" << std::endl;
    std::cout << std::endl << "pi  = " << pi << std::endl;

    // кастуем время работы функции из микро-секунд в мили-секунды
    std::chrono::microseconds microseconds(duration.count());
    std::chrono::seconds seconds = std::chrono::duration_cast<std::chrono::seconds>(microseconds);

    std::cout << "Func time: " << seconds.count() / 1000 << " secs" << std::endl;
}

int main()
{
    setlocale(LC_ALL, "ru");

    task1();
    //task2();
    //task3();

    return 0;
}
