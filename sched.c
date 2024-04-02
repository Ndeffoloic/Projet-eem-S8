#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <unistd.h>
#include <stdbool.h>
#define MAX_JOBS 50
#define MAX_JOB_LENGTH 100
#define DEFAULT_COUNT 3

void print_error(const char* message) {
    fprintf(stderr, "sched: %s\n", message);
}

void print_invalid_file_error(const char* filename) {
    fprintf(stderr, "sched: cannot open file '%s'\n", filename);
}

void print_invalid_workload_format_error() {
    fprintf(stderr, "sched: workload format ([1-4](,[1-4])*\\n)+\n");
}

void print_invalid_schedule_format_error() {
    fprintf(stderr, "sched: schedule format (PID,PID,PID,PID(:PID,PID,PID,PID)*\n)+\n");
}

void print_malloc_failed_error() {
    fprintf(stderr, "malloc failed\n");
}

void parse_workload(const char* workload, int* jobs, int* num_jobs) {
    char* copy = strdup(workload);
    char* token = strtok(copy, "\n");

    int count = 0;
    while (token != NULL) {
        char* inner_token = strtok(token, ",");
        while (inner_token != NULL) {
            if (count >= MAX_JOBS) {
                print_invalid_workload_format_error();
                free(copy);
                exit(1);
            }

            jobs[count] = atoi(inner_token);
            inner_token = strtok(NULL, ",");
            count++;
        }

        token = strtok(NULL, "\n");
    }

    free(copy);
    *num_jobs = count;
}

double jains_fairness_index(double* runtimes, int num_jobs) {
    double sum = 0.0;
    double sum_of_squares = 0.0;
    int num_executed_jobs = 0;

    for (int i = 0; i < num_jobs; i++) {
        if (runtimes[i] > 0) {
            sum += runtimes[i];
            sum_of_squares += pow(runtimes[i], 2);
            num_executed_jobs++;
        }
    }

    if (num_executed_jobs == 0) {
        return 0.0;
    }

    return pow(sum, 2) / (num_executed_jobs * sum_of_squares);
}


void parse_schedule(const char* schedule, int** schedule_matrix, int num_jobs) {
    char* copy = strdup(schedule);
    char* token = strtok(copy, "\n");
    int row = 0;

    while (token != NULL) {

        char* inner_token = strtok(token, ":");
        int col = 0;

        while (inner_token != NULL) {
            char* inner_inner_token = strtok(inner_token, ",");
            while (inner_inner_token != NULL) {

                schedule_matrix[row][col] = atoi(inner_inner_token);
                inner_inner_token = strtok(NULL, ",");
                col++;
            }

            inner_token = strtok(NULL, ":");
        }

        token = strtok(NULL, "\n");
        row++;
    }


    free(copy);
}

void reverse_schedule(int** schedule_matrix, int num_jobs) {
    for (int i = 0; i < num_jobs; i++) {
        for (int j = 0; j < num_jobs / 2; j++) {
            int temp = schedule_matrix[i][j];
            schedule_matrix[i][j] = schedule_matrix[i][num_jobs - j - 1];
            schedule_matrix[i][num_jobs - j - 1] = temp;
        }
    }
}

void print_schedule(int** schedule_matrix, int num_jobs) {
    for (int i = 0; i < num_jobs; i++) {
        for (int j = 0; j < num_jobs; j++) {
            printf("%d", schedule_matrix[i][j]);

            if (j != num_jobs - 1) {
                printf(",");
            }
        }

        printf("\n");
    }
}


int main(int argc, char* argv[]) {
    int period = DEFAULT_COUNT;
    char* schedule_file = NULL;
    char* workload_file = NULL; // Declare workload_file here
    int s_mode = 0;
    int w_mode = 0;
    int compute_fairness = 0;
    int opt;

    while ((opt = getopt(argc, argv, "p:w:s:c")) != -1) {
        switch (opt) {
            case 'p':
                period = atoi(optarg);
                break;
            case 'w':
                workload_file = optarg;
                w_mode = 1;
                break;
            case 's':
                schedule_file = optarg;
                s_mode = 1;
                break;
            case 'c':
                compute_fairness = 1;
                break;
            default:
                print_error("Invalid command line arguments");
                return 1;
        }
    }

    if (period <= 0) {
        print_error("Period must be a positive integer");
        return 1;
    }

    if (compute_fairness == 1 && s_mode !=0 && w_mode ==0) {
        char* schedule;
        if (schedule_file != NULL) {
            FILE* file = fopen(schedule_file, "r");
            if (!file) {
                print_invalid_file_error(schedule_file);
                return 1;
            }

            schedule = malloc(MAX_JOB_LENGTH);
            fgets(schedule, MAX_JOB_LENGTH, file);
            fclose(file);
        } else {
            schedule = malloc(MAX_JOB_LENGTH);
            fgets(schedule, MAX_JOB_LENGTH, stdin);
        }

        int** schedule_matrix = malloc(period * sizeof(int*));
        for (int i = 0; i < period; i++) {
            schedule_matrix[i] = malloc(period * sizeof(int));
        }

        parse_schedule(schedule, schedule_matrix, period);

        double total_fairness_index = 0.0;
        for (int i = 0; i < period; i++) {
            double* runtimes = malloc(period * sizeof(double));
            for (int j = 0; j < period; j++) {
                runtimes[j] = (double)schedule_matrix[i][j] / period;
            }

            total_fairness_index += jains_fairness_index(runtimes, period);
            free(runtimes);
        }

        printf("%.2f%\n", total_fairness_index*100 / period);

        free(schedule);
        for (int i = 0; i < period; i++) {
            free(schedule_matrix[i]);
        }
        free(schedule_matrix);

        return 0;
    }
    if (compute_fairness == 1 && s_mode ==0 && w_mode !=0) {
        char* workload;
        if (workload_file!=NULL) {
            FILE* file = fopen(workload_file, "r");
            if (!file) {
                print_invalid_file_error(workload_file);
                return 1;
            }

            workload = malloc(MAX_JOB_LENGTH);
            fgets(workload, MAX_JOB_LENGTH, file);
            fclose(file);
        } else {
            workload = malloc(MAX_JOB_LENGTH);
            fgets(workload, MAX_JOB_LENGTH, stdin);
        }

        int jobs[MAX_JOBS];
        int num_jobs;
        parse_workload(workload, jobs, &num_jobs);

        double* runtimes = malloc(num_jobs * sizeof(double));
        for (int i = 0; i < num_jobs; i++) {
            runtimes[i] = (double)jobs[i] / period;
        }

        double fairness_index = jains_fairness_index(runtimes, num_jobs);

        int** schedule_matrix = malloc(num_jobs * sizeof(int*));
        for (int i = 0; i < num_jobs; i++) {
            schedule_matrix[i] = malloc(num_jobs * sizeof(int));
        }

        parse_schedule(workload, schedule_matrix, num_jobs);
        reverse_schedule(schedule_matrix, num_jobs);

        if (schedule_file) {
            FILE* file = fopen(schedule_file, "w");
            if (!file) {
                print_invalid_file_error(schedule_file);
                return 1;
            }

            for (int i = 0; i < num_jobs; i++) {
                for (int j = 0; j < num_jobs; j++) {
                    fprintf(file, "%d", schedule_matrix[i][j]);

                    if (j != num_jobs - 1) {
                        fprintf(file, ",");
                    }
                }

                fprintf(file, "\n");
            }

            fclose(file);
        } else {
            print_schedule(schedule_matrix, num_jobs);
        }

        printf("Fairness index: %.2f\n", fairness_index);

        free(workload);
        free(runtimes);
        for (int i = 0; i < num_jobs; i++) {
            free(schedule_matrix[i]);
        }
        free(schedule_matrix);

        return 0;
    }

    if (compute_fairness == 1 && s_mode != 0 && w_mode != 0) {
        // Load workload
        char* workload;
        if (workload_file != NULL) {
            FILE* file = fopen(workload_file, "r");
            if (!file) {
                print_invalid_file_error(workload_file);
                return 1;
            }

            workload = malloc(MAX_JOB_LENGTH);
            fgets(workload, MAX_JOB_LENGTH, file);
            fclose(file);
        } else {
            workload = malloc(MAX_JOB_LENGTH);
            fgets(workload, MAX_JOB_LENGTH, stdin);
        }

        // Load schedule
        char* schedule;
        if (schedule_file != NULL) {
            FILE* file = fopen(schedule_file, "r");
            if (!file) {
                print_invalid_file_error(schedule_file);
                return 1;
            }

            schedule = malloc(MAX_JOB_LENGTH);
            fgets(schedule, MAX_JOB_LENGTH, file);
            fclose(file);
        } else {
            schedule = malloc(MAX_JOB_LENGTH);
            fgets(schedule, MAX_JOB_LENGTH, stdin);
        }
        if (schedule_file != NULL && workload_file != NULL && strcmp(schedule_file, workload_file) == 0) {
            print_error("input and output file must differ");
            return 1;
        }
        // Parse workload and schedule
        int jobs[MAX_JOBS];
        int num_jobs;
        parse_workload(workload, jobs, &num_jobs);

        int** schedule_matrix = malloc(num_jobs * sizeof(int*));
        for (int i = 0; i < num_jobs; i++) {
            schedule_matrix[i] = malloc(num_jobs * sizeof(int));
        }

        parse_schedule(schedule, schedule_matrix, num_jobs);

        // Compute fairness index
        double* runtimes = malloc(num_jobs * sizeof(double));
        for (int i = 0; i < num_jobs; i++) {
            runtimes[i] = (double)jobs[i] / period;
        }

        double fairness_index = jains_fairness_index(runtimes, num_jobs);
        printf("Fairness index: %.2f\n", fairness_index);

        // Cleanup
        free(workload);
        free(schedule);
        free(runtimes);
        for (int i = 0; i < num_jobs; i++) {
            free(schedule_matrix[i]);
        }
        free(schedule_matrix);

        return 0;
    }
}