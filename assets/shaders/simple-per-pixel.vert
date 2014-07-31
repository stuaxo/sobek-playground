#version 120

attribute vec3 vertex;
attribute vec3 normal;

uniform mat4 sobek_ModelMatrix;
uniform mat4 sobek_ProjectionMatrix;
uniform mat3 sobek_NormalMatrix;

varying vec3 v;
varying vec3 n;

void main() {
	v = vec3(sobek_ModelMatrix * vec4(vertex, 1.0));
	n = sobek_NormalMatrix * normal;

	gl_Position = sobek_ProjectionMatrix * sobek_ModelMatrix * vec4(vertex, 1.0);
}

