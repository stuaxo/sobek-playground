attribute vec3 vertex;
attribute vec2 uv;

uniform mat4 sobek_ModelMatrix;
uniform mat4 sobek_ProjectionMatrix;

varying vec2 t;

// We use this simple matrix to invert our image coorindates, since we
// know they're going to be flipped. HOWEVER, this is just a hack.
const mat2 tm = mat2(1, 0, 0, -1);

void main() {
	// t = tm * uv;
	t = vec2(uv.x, 1.0 - uv.y);

	gl_Position = sobek_ProjectionMatrix * sobek_ModelMatrix * vec4(vertex, 1.0);
}

