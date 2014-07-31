#version 120

attribute vec3 vertex;
attribute vec3 normal;
attribute vec4 index;
attribute vec4 weight;

uniform mat4 sobek_ModelMatrix;
uniform mat4 sobek_ProjectionMatrix;
uniform mat3 sobek_NormalMatrix;

uniform mat4 bones[80];

varying vec3 v;
varying vec3 n;

void main() {
	mat4 m = bones[int(index.x)] * weight.x;
	
	m += bones[int(index.y)] * weight.y;
	m += bones[int(index.z)] * weight.z;
	m += bones[int(index.w)] * weight.w;

	vec4 pos = m * vec4(vertex, 1.0);

	v = pos.xyz / pos.w;
	// v = vertex;

	// TODO: This is NOT the proper transformation of the normal (I don't think).
	// But it might be sufficient for most animations.
	n = mat3(m) * (sobek_NormalMatrix * normal);
	// n = sobek_NormalMatrix * (mat3(m) * normal);
	// n = sobek_NormalMatrix * normal;

	gl_Position = sobek_ProjectionMatrix * sobek_ModelMatrix * pos;
	// gl_Position = sobek_ProjectionMatrix * sobek_ModelMatrix * vec4(vertex, 1.0);
}

