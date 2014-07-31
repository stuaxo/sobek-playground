#version 120

attribute vec3 vertex;
attribute vec3 normal;
attribute vec2 uv;

uniform mat4 sobek_ModelMatrix;
uniform mat4 sobek_ProjectionMatrix;
uniform mat3 sobek_NormalMatrix;

varying vec3 n;
varying vec2 t;

void main() {
	t = uv;
	n = normalize(sobek_NormalMatrix * normal);

	gl_Position = sobek_ProjectionMatrix * sobek_ModelMatrix * vec4(vertex, 1.0);
}

