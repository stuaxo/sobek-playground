#version 120

attribute vec3 vertex;
attribute vec3 bc;

uniform mat4 sobek_ModelMatrix;
uniform mat4 sobek_ProjectionMatrix;

varying vec3 b;

void main() {
	b = bc;

	gl_Position = sobek_ProjectionMatrix * sobek_ModelMatrix * vec4(vertex, 1.0);
}

