import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'camera_screen.dart';

class QuestionnaireScreen extends StatefulWidget {
  final String colorBlindnessType;
  final String selectedSeverity;

  const QuestionnaireScreen({
    Key? key,
    required this.colorBlindnessType,
    required this.selectedSeverity,
  }) : super(key: key);

  @override
  _QuestionnaireScreenState createState() => _QuestionnaireScreenState();
}

class _QuestionnaireScreenState extends State<QuestionnaireScreen> {
  List<dynamic> questions = [];
  int currentIndex = 0;
  Map<int, String> answers = {};

  @override
  void initState() {
    super.initState();
    _loadQuestions();
  }

  Future<void> _loadQuestions() async {
    try {
      final String response = await rootBundle.loadString('assets/questions.json');
      final data = json.decode(response);
      setState(() {
        questions = data[widget.colorBlindnessType] ?? [];
      });
    } catch (e) {
      print("Error loading questions: $e");
    }
  }

  void _navigateNextQuestion(String answer) {
    setState(() {
      answers[currentIndex] = answer;
      if (currentIndex < questions.length - 1) {
        currentIndex++;
      } else {
        _evaluateSeverityLevel();
      }
    });
  }

  void _previousQuestion() {
    setState(() {
      if (currentIndex > 0) {
        currentIndex--;
      }
    });
  }

  void _evaluateSeverityLevel() {
    int countA = answers.values.where((a) => a.startsWith('A')).length;
    int countB = answers.values.where((a) => a.startsWith('B')).length;
    int countC = answers.values.where((a) => a.startsWith('C')).length;

    String severity = countA > countB && countA > countC
        ? "Severe"
        : countB > countC
            ? "Moderate"
            : "Mild";

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text("Assessment Result"),
        content: Text("Your color blindness severity: $severity"),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              Navigator.pushReplacement(
                context,
                MaterialPageRoute(
                  builder: (context) => CameraScreen(
                    selectedColorBlindnessType: widget.colorBlindnessType,
                    selectedColorBlindnessSeverity: severity,
                  ),
                ),
              );
            },
            child: Text("OK"),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (questions.isEmpty) {
      return Scaffold(body: Center(child: CircularProgressIndicator()));
    }

    var questionData = questions[currentIndex];
    double progress = currentIndex / questions.length;

    return Scaffold(
      appBar: AppBar(title: Text("Question ${currentIndex + 1} of ${questions.length}")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            LinearProgressIndicator(
              value: progress,
              minHeight: 5,
              backgroundColor: Colors.grey[200],
              color: Colors.blue,
            ),
            SizedBox(height: 20),
            Text(
              questionData["question"],
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 20),
            ...List.generate(questionData["options"].length, (index) {
              String option = questionData["options"][index];
              return GestureDetector(
                onTap: () => _navigateNextQuestion(option),
                child: Container(
                  margin: EdgeInsets.only(bottom: 10),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(10),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.grey.withOpacity(0.2),
                        spreadRadius: 2,
                        blurRadius: 5,
                        offset: Offset(0, 3),
                      ),
                    ],
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Text(
                      option,
                      style: TextStyle(fontSize: 18, color: Colors.black87),
                    ),
                  ),
                ),
              );
            }),
            SizedBox(height: 20),
            Visibility(
              visible: currentIndex > 0,
              child: ElevatedButton(
                onPressed: _previousQuestion,
                child: Text('Previous Question'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
