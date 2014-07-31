uniform sampler2D texture;

varying vec2 t;

void main() {
	gl_FragColor = texture2D(texture, t);
}

