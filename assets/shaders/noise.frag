#version 120

uniform float     sobek_Timer;
uniform sampler2D texture;

varying vec3 n;
varying vec2 t;

const float D  = 4.0;
const float D2 = D / 2.0;

void main() {
	float d = 1.0 - (abs(mod(mod(sobek_Timer, D), D) - D2) / D2);

	gl_FragColor = d * vec4(0.6, 0.8, 1.0, 1.0) * texture2D(texture, t) * max(dot(n, vec3(1.0, 1.0, 1.0)), 0.0);

	gl_FragColor.a = 1.0;
}

