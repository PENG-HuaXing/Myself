#ifndef MATRIX_H_
#define MATRIX_H_


class Matrix

{
        private:
                double **A;
                int columns;
                int rows;
        public:
                Matrix();
                Matrix(double **B, int m, int n);
                Matrix(const Matrix &);
                ~Matrix();
                double item(int i, int j) const;
				void changeitem(double,int ,int);
                double ** valueaddress() const;
                int fcolumns() const;
                int frows() const;
                void showinfo() const;
                Matrix &  operator=(const Matrix & B);
                Matrix operator+(const Matrix & B) const;
                Matrix operator-(const Matrix & B) const;
                Matrix operator*(const Matrix & B) const;

};

#endif
