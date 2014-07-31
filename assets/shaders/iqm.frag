#version 120

uniform vec4 color;

varying vec3 v;
varying vec3 n;

const vec3 LIGHT = vec3(0.0, 1.0, 1.0);

void main() {
	float d = length(LIGHT - v);
	vec3  l = normalize(LIGHT - v);

	float diffuse = max(dot(n, l), 0.1);

	diffuse = diffuse * (1.0 / (1.0 + (0.25 * d * d)));
	
	gl_FragColor = color * diffuse;
}

