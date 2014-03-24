function [cl,cX,cY,cZ] = waterCluster2(band1,band2,band3,nC)
	% This is a quick script that uses a simple unsupervised machine 
	% learning algorithm, k-means clustering, to classify data 
	% according to water type.
	% 
	% Inputs: 
	% - bandX => 3 wavebands (e.g. 443,510,555, cf: Martin Traykovski & Sosik., 2003, JGR,108(C5),3150)
	% - nC    => number of clusters to be found	  
	% Outputs:
	% -cl => cluster flag, ranges from 1 to nC, cluster that data are assigned to.
	% -cX, cY, cZ = > cluster coordinates, size (nCx1)
	warning off
	% This script requires the octave geometry package. On lionfish
	% this is located at :
	addpath('/disk01/home/ekarakoy/geometry')
	if nC > 6
		disp('too many clusters invoked, reducing to 6')
		nC = 6;
	end
    %Random initialization of the 3 cluster centroids
	max1 = max(band1); min1 = min(band1);
    max2 = max(band2); min2 = min(band2);
    max3 = max(band3); min3 = min(band3);
    % define coordinates for 3 centroids
	centsX = rand(nC,1) * (max1 - min1) + min1;
    centsY = rand(nC,1) * (max2 - min2) + min2;
    centsZ = rand(nC,1) * (max3 - min3) + min3;
    lenData = length(band1); % number of examples
    cluster = zeros(lenData,1); % can take values 1,2,3 to denote cluster membership for 
                                % each example
    % For now skip defining thresh and alpha, just loop m times
	

    % Plotting an initial figure
	plotColors='rgbmck';
	figure
	% calculate distance to randomly initialize centroid
	cluster = assignToCluster(band1,band2,band3,centsX,centsY,centsZ,nC);

	for jk = 1:nC
		hx(jk) = plot3(centsX(jk),centsY(jk),centsZ(jk),'x'); hold on
		set(hx(jk),'markersize',12,'linewidth',2,'color',plotColors(jk))
		hp(jk) = plot3(band1(cluster==jk),band2(cluster==jk),band3(cluster==jk),'.');
		set(hp(jk),'markersize',16,'color',plotColors(jk))
	end

	drawnow
	pause(0.5)
	mcd = 1;
	thresh = 0.01;

	% continue with computation
	while mcd > thresh
		% Part I ---- assign points to old cluster centroid
	    cluster = assignToCluster(band1,band2,band3,centsX,centsY,centsZ,nC);
		oldCentsX = centsX;
		oldCentsY = centsY;
		oldCentsZ = centsZ;	
		for jk = 1:nC

			if sum(cluster==jk) > 0
				centsX(jk,1) = mean(band1(cluster == jk));
				centsY(jk,1) = mean(band2(cluster == jk));
				centsZ(jk,1) = mean(band3(cluster == jk));
			else
				centsX(jk,1) = rand(1) * (max1 - min1) + min1;
				centsY(jk,1) = rand(1) * (max2 - min2) + min2;
				centsZ(jk,1) = rand(1) * (max3 - min3) + min3;
			end
			set(hx(jk),'xdata',centsX(jk),'ydata',centsY(jk),'zdata',centsZ(jk))
			delete(hp(jk))
			hp(jk) = plot3(band1(cluster==jk),band2(cluster==jk),band3(cluster==jk),'.');
			set(hp(jk),'markersize',16,'color',plotColors(jk))
			drawnow
			pause(0.5)
		end
		centDist = distancePoints([centsX,centsY,centsZ],[oldCentsX,oldCentsY,oldCentsZ]);
		% this gives nC^2 distances in a nC x nC mat. We only want the biggest of the nCs on the diagonal:
		mcd = max(diag(centDist));		
    end
	cl = cluster;
	cX = centsX;
	cY = centsY;
	cZ = centsZ;
end
function cluster = assignToCluster(rrs1,rrs2,rrs3,cx,cy,cz,nc)
	
	d = distancePoints([rrs1,rrs2,rrs3],[cx,cy,cz]);
	cluster = (d == min(d,[],2)) * (1:nc)'; % assign centroid index (1, 2, or 3)
end
