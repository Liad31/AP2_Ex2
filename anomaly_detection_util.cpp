/*
 * animaly_detection_util.cpp
 *
 *  Created on: 11 ����� 2020
 *      Author: Eli
 */

#include "anomaly_detection_util.h"
#include <cmath>
#include <vector>
	float avg(float* x, int size) {
		float sum = 0;
		for (int i = 0; i < size; sum += x[i], i++);
		return sum / size;
	}

	// returns the variance of X and Y
	float var(float* x, int size) {
		float av = avg(x, size);
		float sum = 0;
		for (int i = 0; i < size; i++) {
			sum += x[i] * x[i];
		}
		return sum / size - av * av;
	}

	// returns the covariance of X and Y
	float cov(float* x, float* y, int size) {
		float sum = 0;
		for (int i = 0; i < size; i++) {
			sum += x[i] * y[i];
		}
		sum /= size;

		return sum - avg(x, size) * avg(y, size);
	}


	// returns the Pearson correlation coefficient of X and Y
	float pearson(float* x, float* y, int size) {
		return cov(x, y, size) / (sqrt(var(x, size)) * sqrt(var(y, size)));
	}

	// performs a linear regression and returns the line equation
	Line linear_reg(Point** points, int size) {
		std::vector<float> x(size), y(size);
		for (int i = 0; i < size; i++) {
			x[i] = points[i]->x;
			y[i] = points[i]->y;
		}
		float a = cov(&x[0], &y[0], size) / var(&x[0], size);
		float b = avg(&y[0], size) - a * (avg(&x[0], size));

		return Line(a, b);
	}

	// returns the deviation between point p and the line equation of the points
	float dev(Point p, Point** points, int size) {
		Line l = linear_reg(points, size);
		return dev(p, l);
	}

	// returns the deviation between point p and the line
	float dev(Point p, Line l) {
		return std::abs(p.y - l.f(p.x));
	}



