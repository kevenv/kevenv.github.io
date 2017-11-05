"use strict";

var gridH = [];
var grad = [];

function createGrid(w,h)
{
	//grid.data = new Array(w);
	for(var i = 0; i < w; i++) {
		grid.push([]);
		gridH.push([]);
		grad.push([]);
		for(var j = 0; j < h; j++) {
			grid[i].push(0);
			gridH[i].push(0);
			grad[i].push(0);
		}
	}
}

function waveEq(y0, f, t, x, c, phase)
{
	var w = 2*Math.PI*f;
	return y0 * Math.cos(w * (t - x/c) + phase*Math.PI);
}

function waveEq2DNoDist(a,f,t,c,phase)
{
	var temp1 = new THREE.Vector2(0,0);
	var temp2 = new THREE.Vector2(0,0);
	return waveEq2D(a,temp1,temp2,f,t,c,phase);
}

function waveEq2D(amplitude,sensorLocation,sourceLocation,f,t,c,phase)
{
	var length = sensorLocation.distanceTo(sourceLocation);
	var amp = waveEq(amplitude, f, t, length, c, phase);
	return amp;
}

var oldAlgorithm = false;


function resetGrid()
{
	for(var i = 0; i < gridWidth; i++) {
		for(var j = 0; j < gridHeight; j++) {
			grid[i][j] = 0.0;
			gridH[i][j] = 0.0;
		}
	}
}
function resetSource(){
	for (var i = 0; i < spheres.length; i++){
		scene.remove(spheres[i]);
	}
	sources = [];
	spheres = [];
    addSrc(sourceA.x, sourceA.y, 0, sourceA.vx, sourceA.vy, sourceA.fx, sourceA.fy);
    addSrc(sourceB.x, sourceB.y, 0, sourceB.vx, sourceB.vy, sourceB.fx, sourceB.fy);
}

function clamp (min,max,value)
{
  return Math.min(Math.max(value, min), max);
}

function tickSim(t, sources, frequency, waveSpeed, amplitude, Damping, deltaT)
{
	var f = frequency;
	var c = waveSpeed;
	var a = amplitude;
	
	for (var s = 0; s < sources.length; ++s)
	{
		var source = sources[s];
		
		if (Math.abs(source.fx - source.x) > 2.0)
			source.fx = source.x;
		if (Math.abs(source.fy - source.y) > 2.0)
			source.fy = source.y

		source.fx += source.vx * deltaT*8.0;
		source.fy += source.vy * deltaT*8.0;
		source.x = clamp(0, 199, Math.round(source.fx));
		source.y = clamp(0, 199, Math.round(source.fy));
	}

	if (params.switch_Algorithm)
	{
		if (!oldAlgorithm)
		{
			oldAlgorithm = true;
			resetGrid();
		}
		// new physics engine!
		var dt = deltaT;
		var damping = Damping;
		updateField(dt,damping,t,frequency,waveSpeed,amplitude);
	}
	else
	{
		if (oldAlgorithm)
		{
			oldAlgorithm = false;
			resetGrid();
		}
		// update amplitudes
		var dt = clock.getDelta();
		for(var i = 0; i < gridWidth; i++) {
			for(var j = 0; j < gridHeight; j++) {
				grid[i][j] = 0.0;
				for (var s = 0; s < sources.length; ++s)
				{
					var sensorLocation = new THREE.Vector2(i, j);
					var sourceLocation = new THREE.Vector2(sources[s].x, sources[s].y);
					grid[i][j] += waveEq2D(a,sensorLocation,sourceLocation,f,t,c, sources[s].phase);
				}
			}
		}
	}

	currentTime += dt;
}

function updateField(dt,damping,t,frequency,wavespeed,amplitude)
{
	for(var i = 0; i < gridWidth; i++) {
		for(var j = 0; j < gridHeight; j++) {
			var deltaX = 0.1;
			var deltaY = 0.1;
			var gradX = (getGrid(i+1,j) - 2.0*getGrid(i,j) + getGrid(i-1,j)) / (deltaX*deltaX);
			var gradY = (getGrid(i,j+1) - 2.0*getGrid(i,j) + getGrid(i,j-1)) / (deltaY*deltaY);
			grad[i][j] = gradX + gradY;

			gridH[i][j] += dt * (grad[i][j] - damping*gridH[i][j]);
			grid[i][j] += dt * gridH[i][j];
		}
	}

	var k = 1;
	for(var s = 0; s < sources.length; ++s) {
		var src = sources[s];
		grid[src.x][src.y] = waveEq2DNoDist(amplitude, frequency, t, wavespeed, src.phase);
	}
}

function getGrid(i, j)
{
	if(i >= 0 && i <= gridWidth-1 &&
		j >= 0 && j <= gridHeight-1) 
	{
		return grid[i][j];
	}
	else {
		var newI = i;
		var newJ = j;
		if(i < 0) {
			newI = i+1;
		}
		if(i > gridWidth-1) {
			newI = i-1;
		}
		if(j < 0) {
			newJ = j+1;
		}
		if(j > gridHeight-1) {
			newJ = j-1;
		}
		return grid[newI][newJ];
	}
}
