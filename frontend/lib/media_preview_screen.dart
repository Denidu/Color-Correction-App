import 'dart:io';
import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';

class MediaPreviewScreen extends StatefulWidget {
  final String originalMediaPath;
  final String correctedMediaUrl;
  final bool isVideo;

  const MediaPreviewScreen({
    Key? key,
    required this.originalMediaPath,
    required this.correctedMediaUrl,
    required this.isVideo,
  }) : super(key: key);

  @override
  _MediaPreviewScreenState createState() => _MediaPreviewScreenState();
}

class _MediaPreviewScreenState extends State<MediaPreviewScreen> {
  VideoPlayerController? _originalController;
  VideoPlayerController? _correctedController;

  @override
  void initState() {
    super.initState();

    if (widget.isVideo) {
      _originalController = VideoPlayerController.file(File(widget.originalMediaPath))
        ..initialize().then((_) {
          setState(() {});
          _originalController!.play();
        });

      _correctedController = VideoPlayerController.network(widget.correctedMediaUrl)
        ..initialize().then((_) {
          setState(() {});
        });
    }
  }

  @override
  void dispose() {
    _originalController?.dispose();
    _correctedController?.dispose();
    super.dispose();
  }

 @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Media Preview")),
      body: SingleChildScrollView(
        child: Column(
          children: [
            Container(
              padding: const EdgeInsets.all(8.0),
              child: Column(
                children: [
                  const Text("Captured Media",
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  widget.isVideo
                      ? (_originalController != null &&
                              _originalController!.value.isInitialized
                          ? AspectRatio(
                              aspectRatio: _originalController!.value.aspectRatio,
                              child: VideoPlayer(_originalController!),
                            )
                          : const CircularProgressIndicator())
                      : Image.file(File(widget.originalMediaPath),
                          fit: BoxFit.contain),
                ],
              ),
            ),

            const SizedBox(height: 20),

            Container(
              padding: const EdgeInsets.all(8.0),
              child: Column(
                children: [
                  const Text("Corrected Media",
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  if (widget.isVideo) 
                    (_correctedController != null &&
                            _correctedController!.value.isInitialized
                        ? AspectRatio(
                            aspectRatio: _correctedController!.value.aspectRatio,
                            child: VideoPlayer(_correctedController!),
                          )
                        : const CircularProgressIndicator())
                  else
                    Image.network(widget.correctedMediaUrl, fit: BoxFit.contain),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}