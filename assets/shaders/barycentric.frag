#version 120
#extension GL_OES_standard_derivatives: enable

varying vec3 b;

float edge_factor() {
	vec3 d  = fwidth(b);
	vec3 a3 = smoothstep(vec3(0.0), d * 1.25, b);

	return min(min(a3.x, a3.y), a3.z);
}

void main() {
	gl_FragColor.rgb = mix(vec3(0.0), vec3(0.5), edge_factor());

	// gl_FragColor = vec4(0.0, 0.0, 0.0, (1.0 - edge_factor()) * 0.95);
}

