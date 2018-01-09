Frame GetBestFrame(std::vector<Frame> frames)
{
	Frame bestFrame = NULL;
	int maxPoseCount = 0;

	for (int i = 0; i < frames.Count; ++i)
	{
		Frame frame = frames[i];
		int count = frame.Poses.size();
		if(count > maxPoseCount){
			bestFrame = frame;
			maxPoseCount = count;		
		}
	}
	return bestFrame;
}

Frame GetBestFrame2(std::vector<Frame> frames)
{
	Frame bestFrame = NULL;
	int maxFaceCount = 0;

	for (int i = 0; i < frames.Count; ++i)
	{
		Frame frame = frames[i];
		int count = frame.Faces.size();
		if(count > maxPoseCount){
			bestFrame = frame;
			maxFaceCount = count;		
		}
	}
	return bestFrame;
}

/*
Ideen / Anmerkungen :

Eine Pose kann auf verschiedene Weisen analysiert und gewertet werden.
Jede Pose/Frame muss gewichtet werden (0-1) anhand von :
1) Anzahl der Nodes jeder Pose
2) Anzahl der Posen (personen)
3) Gesichtsnodes (Schaut person zu kamer oder nicht, priorisierung?)
4) Abstände der einzelnen Nodes, bzw Länge der Joints (Graphen Klasse PAD?) 
5) Wertigkeit der Pose über eine gewisse Zeitspanne (mehrere Frames) -> Wechsel bei zu schlechter Wertigkeit
*/