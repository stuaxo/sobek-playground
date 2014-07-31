uniform sampler2D texture;

varying vec2 t;

const float vi_inner = 0.0;
const float vi_outer = 0.75;

void main() {
	vec4  c        = texture2D(texture, t);
	float dist     = distance(t, vec2(0.5, 0.5));
	float vignette = smoothstep(vi_outer, vi_inner, dist);

	// gl_FragColor = vec4(vignette, vignette, vignette, 1.0);

	gl_FragColor = vec4(
		dot(c.rgb, vec3(0.393, 0.769, 0.189)) * vignette,
		dot(c.rgb, vec3(0.349, 0.686, 0.168)) * vignette,
		dot(c.rgb, vec3(0.272, 0.534, 0.131)) * vignette,
		c.a
	);
}

