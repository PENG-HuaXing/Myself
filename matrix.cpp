
#include<iostream>
#include "matrix.h"
using std::cout;
using std::cin;


Matrix::Matrix()
{
        A=new double *;
        A[0]= new double;
        A[0][0]=0;
        rows=1;columns=1;
}
Matrix::Matrix(double ** B,int m,int n)
{

        columns = n;
        rows = m;
        A=new double * [rows];
        for (int i=0;i<rows;i++)
                A[i]=new double [columns];
        for(int i=0;i<rows;i++)
                for (int j=0;j<columns;j++)
                        A[i][j]=B[i][j];
}

Matrix::Matrix(const Matrix & B)
{
        rows=B.frows();
        columns=B.fcolumns();
        A=new double * [rows];
        for (int i=0;i<rows;i++)
                A[i]=new double [columns];
        for (int i=0;i<rows;i++)
                for (int j=0;j<columns;j++)
                        A[i][j]=B.item(i,j);
}

double Matrix::item(int i, int j) const
{
        return A[i][j];
}

void Matrix::changeitem(double a,int m,int n)
{
	if((m<rows&&m>=0) && (n<columns&&n>=0))
		A[m][n]=a;
	else
		cout << "The item is not exist";
}

double ** Matrix::valueaddress() const
{
        return A;
}
int Matrix::fcolumns() const
{
        return columns;
}
int Matrix::frows() const
{
        return rows;
}
void Matrix::showinfo() const
{
        for (int i=0;i<rows;i++)
                {
                        for (int j=0;j<columns;j++)
                                cout << A[i][j] << "\t";
                        cout << "\n";
                }
        cout << "rows: " << rows << "\t";
        cout << "columns" << columns << "\n";
}

Matrix &  Matrix::operator=(const Matrix & B)
{
        if(&B==this)
                return * this;
        else
        {
                for(int i=0;i<rows;i++)
                        delete []A[i];
                delete []A;

                rows=B.frows();
                columns=B.fcolumns();
                A=new double * [rows];
                for (int i=0;i<rows;i++)
                        A[i]=new double [columns];
                for (int i=0;i<rows;i++)
                        for (int j=0;j<columns;j++)
                                A[i][j]=B.item(i,j);
                return * this;
        }
}

Matrix Matrix::operator+(const Matrix & B) const
{

        if(rows==B.rows&&columns==B.columns)
        {
                double ** C;
                C=new double *[rows];
                for(int i=0;i<rows;i++)
                        C[i]=new double [columns];
                for(int i=0;i<rows;i++)
                        for(int j=0;j<columns;j++)
                                C[i][j]=A[i][j]+B.item(i,j);
                return Matrix(C,rows,columns);
        }
        else
        {
                cout << "Can't sum together!!";
                return Matrix();
        }

}

Matrix Matrix::operator-(const Matrix & B) const
{
        if(rows==B.rows&&columns==B.columns)
        {
                double **C;
                C=new double *[rows];
                for(int i=0;i<rows;i++)
                        C[i]=new double [columns];
                for(int i=0;i<rows;i++)
                        for(int j=0;j<columns;j++)
                                C[i][j]=A[i][j]-B.item(i,j);
                return Matrix(C,rows,columns);
        }
        else
        {
                cout << "Can't min together!!";
                return Matrix();
        }
}

Matrix Matrix::operator*(const Matrix & B) const
{

        if(columns==B.frows())
        {
                double **C;
                C=new double* [rows];
                for(int i=0;i<rows;i++)
                        C[i]=new double [B.fcolumns()];

                for(int i=0;i<rows;i++)
                        for(int j=0;j<B.fcolumns();j++)
                                {
                                        C[i][j]=0;
                                        for (int m=0;m<columns;m++)
                                                C[i][j]=C[i][j]+A[i][m]*B.item(m,j);
                                }

                return Matrix(C,rows,B.fcolumns());
        }
        else
        {
                cout << "Can't muli together!!";
                return Matrix();
        }
}

Matrix::~Matrix()
{
        for (int i = 0; i < rows; i++)
                delete []A[i];
        delete []A;
}

