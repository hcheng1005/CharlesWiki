# 卡尔曼

$$
\begin{aligned}
\overline{\mathbf x} &= \mathbf{Fx} + \mathbf{Bu} \\
\overline{\mathbf P} &=  \mathbf{FPF}^\mathsf{T} + \mathbf Q \\ \\
\mathbf y &= \mathbf z - \mathbf{H}\overline{\mathbf x} \\
\mathbf S &= \mathbf{H}\overline{\mathbf P}\mathbf{H}^\mathsf{T} + \mathbf R \\
\mathbf K &= \overline{\mathbf P}\mathbf{H}^\mathsf{T}\mathbf{S}^{-1} \\ \\
\mathbf x  &= \overline{\mathbf x} +\mathbf{Ky} \\
\mathbf P &= (\mathbf{I}-\mathbf{KH})\overline{\mathbf P}
\end{aligned}$$
---

## 目录
- [Table of Contents](Kalman-and-Bayesian-Filters-in-Python/table_of_contents.ipynb)
---

## 子章节
- [06-Multivariate-Kalman-Filters](Kalman-and-Bayesian-Filters-in-Python/06-Multivariate-Kalman-Filters.ipynb)
- [Q R noise](Kalman-and-Bayesian-Filters-in-Python/07-Kalman-Filter-Math.ipynb)
