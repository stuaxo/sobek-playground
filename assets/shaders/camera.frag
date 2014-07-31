#version 120

varying vec3 n;

void main() {
	gl_FragColor = vec4(0.6, 0.8, 1.0, 1.0) * max(dot(n, vec3(0.0, 1.0, 1.0)), 0.0);
}

