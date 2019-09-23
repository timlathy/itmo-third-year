main() {
    int A[10] = {2, 5, -8, 7, -3, 15, 38, -11, 66, -6};
    int I, S, P;
    S = 0;
    P = 1;
    for (I = 1; I < 10; I++) {
        P *= A[I];
        if (A[I] < 0) {
            S += A[I];
        }
    }
    return 0;
}
