# Flutter Integration Guide for DiaWell API

## 🚀 Quick Start

### 1. Add HTTP Dependency
Add to your `pubspec.yaml`:
```yaml
dependencies:
  http: ^1.1.0
```

### 2. Import the API Client
```dart
import 'flutter_api_client.dart';
```

### 3. Basic Usage
```dart
// Health check
final health = await DiaWellApiClient.healthCheck();
print('API Status: ${health['status']}');

// Submit risk assessment
final result = await DiaWellApiClient.submitRiskAssessment(
  name: 'John Doe',
  age: 45,
  gender: 'male',
  height: 175.0,
  weight: 80.0,
  bpSys: 140,
  bpDia: 90,
  historyHighGlucose: false,
  physicalActivityHoursPerWeek: 3.0,
  familyHistoryDiabetes: 'none',
  smokingStatus: 'never',
  alcoholStatus: 'moderate',
);

print('Risk Score: ${result['risk_score']}');
print('Risk Level: ${result['risk_level']}');
```

## 📱 Complete Flutter Widget Example

```dart
import 'package:flutter/material.dart';
import 'flutter_api_client.dart';

class RiskAssessmentScreen extends StatefulWidget {
  @override
  _RiskAssessmentScreenState createState() => _RiskAssessmentScreenState();
}

class _RiskAssessmentScreenState extends State<RiskAssessmentScreen> {
  final _formKey = GlobalKey<FormState>();
  bool _isLoading = false;
  Map<String, dynamic>? _result;
  
  // Form controllers
  final _nameController = TextEditingController();
  final _ageController = TextEditingController();
  final _heightController = TextEditingController();
  final _weightController = TextEditingController();
  final _bpSysController = TextEditingController();
  final _bpDiaController = TextEditingController();
  
  String _gender = 'male';
  bool _historyHighGlucose = false;
  double _physicalActivity = 3.0;
  String _familyHistory = 'none';
  String _smokingStatus = 'never';
  String _alcoholStatus = 'moderate';
  
  Future<void> _submitAssessment() async {
    if (!_formKey.currentState!.validate()) return;
    
    setState(() => _isLoading = true);
    
    try {
      final result = await DiaWellApiClient.submitRiskAssessment(
        name: _nameController.text,
        age: int.parse(_ageController.text),
        gender: _gender,
        height: double.parse(_heightController.text),
        weight: double.parse(_weightController.text),
        bpSys: int.parse(_bpSysController.text),
        bpDia: int.parse(_bpDiaController.text),
        historyHighGlucose: _historyHighGlucose,
        physicalActivityHoursPerWeek: _physicalActivity,
        familyHistoryDiabetes: _familyHistory,
        smokingStatus: _smokingStatus,
        alcoholStatus: _alcoholStatus,
      );
      
      setState(() {
        _result = result;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('DiaWell Risk Assessment'),
        backgroundColor: Colors.blue[600],
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Basic Information
              _buildSection('Basic Information', [
                TextFormField(
                  controller: _nameController,
                  decoration: InputDecoration(labelText: 'Full Name'),
                  validator: (value) => value?.isEmpty == true ? 'Required' : null,
                ),
                SizedBox(height: 16),
                TextFormField(
                  controller: _ageController,
                  decoration: InputDecoration(labelText: 'Age'),
                  keyboardType: TextInputType.number,
                  validator: (value) => value?.isEmpty == true ? 'Required' : null,
                ),
                SizedBox(height: 16),
                DropdownButtonFormField<String>(
                  value: _gender,
                  decoration: InputDecoration(labelText: 'Gender'),
                  items: ['male', 'female', 'other'].map((gender) {
                    return DropdownMenuItem(value: gender, child: Text(gender));
                  }).toList(),
                  onChanged: (value) => setState(() => _gender = value!),
                ),
              ]),
              
              // Physical Measurements
              _buildSection('Physical Measurements', [
                TextFormField(
                  controller: _heightController,
                  decoration: InputDecoration(labelText: 'Height (cm)'),
                  keyboardType: TextInputType.number,
                  validator: (value) => value?.isEmpty == true ? 'Required' : null,
                ),
                SizedBox(height: 16),
                TextFormField(
                  controller: _weightController,
                  decoration: InputDecoration(labelText: 'Weight (kg)'),
                  keyboardType: TextInputType.number,
                  validator: (value) => value?.isEmpty == true ? 'Required' : null,
                ),
                SizedBox(height: 16),
                Row(
                  children: [
                    Expanded(
                      child: TextFormField(
                        controller: _bpSysController,
                        decoration: InputDecoration(labelText: 'Systolic BP'),
                        keyboardType: TextInputType.number,
                        validator: (value) => value?.isEmpty == true ? 'Required' : null,
                      ),
                    ),
                    SizedBox(width: 16),
                    Expanded(
                      child: TextFormField(
                        controller: _bpDiaController,
                        decoration: InputDecoration(labelText: 'Diastolic BP'),
                        keyboardType: TextInputType.number,
                        validator: (value) => value?.isEmpty == true ? 'Required' : null,
                      ),
                    ),
                  ],
                ),
              ]),
              
              // Medical History
              _buildSection('Medical History', [
                SwitchListTile(
                  title: Text('History of High Glucose'),
                  value: _historyHighGlucose,
                  onChanged: (value) => setState(() => _historyHighGlucose = value),
                ),
                SizedBox(height: 16),
                DropdownButtonFormField<String>(
                  value: _familyHistory,
                  decoration: InputDecoration(labelText: 'Family History of Diabetes'),
                  items: [
                    DropdownMenuItem(value: 'none', child: Text('None')),
                    DropdownMenuItem(value: 'second_degree', child: Text('Second-degree relative')),
                    DropdownMenuItem(value: 'first_degree', child: Text('First-degree relative')),
                  ],
                  onChanged: (value) => setState(() => _familyHistory = value!),
                ),
              ]),
              
              // Lifestyle Factors
              _buildSection('Lifestyle Factors', [
                Text('Physical Activity: ${_physicalActivity.toStringAsFixed(1)} hours/week'),
                Slider(
                  value: _physicalActivity,
                  min: 0,
                  max: 20,
                  divisions: 40,
                  onChanged: (value) => setState(() => _physicalActivity = value),
                ),
                SizedBox(height: 16),
                DropdownButtonFormField<String>(
                  value: _smokingStatus,
                  decoration: InputDecoration(labelText: 'Smoking Status'),
                  items: [
                    DropdownMenuItem(value: 'never', child: Text('Never smoked')),
                    DropdownMenuItem(value: 'former', child: Text('Former smoker')),
                    DropdownMenuItem(value: 'moderate', child: Text('Moderate smoker')),
                    DropdownMenuItem(value: 'current', child: Text('Current smoker')),
                    DropdownMenuItem(value: 'heavy', child: Text('Heavy smoker')),
                  ],
                  onChanged: (value) => setState(() => _smokingStatus = value!),
                ),
                SizedBox(height: 16),
                DropdownButtonFormField<String>(
                  value: _alcoholStatus,
                  decoration: InputDecoration(labelText: 'Alcohol Consumption'),
                  items: [
                    DropdownMenuItem(value: 'never', child: Text('Never drink')),
                    DropdownMenuItem(value: 'former', child: Text('Former drinker')),
                    DropdownMenuItem(value: 'moderate', child: Text('Moderate drinker')),
                    DropdownMenuItem(value: 'current', child: Text('Current drinker')),
                    DropdownMenuItem(value: 'heavy', child: Text('Heavy drinker')),
                  ],
                  onChanged: (value) => setState(() => _alcoholStatus = value!),
                ),
              ]),
              
              SizedBox(height: 24),
              
              // Submit Button
              ElevatedButton(
                onPressed: _isLoading ? null : _submitAssessment,
                style: ElevatedButton.styleFrom(
                  padding: EdgeInsets.symmetric(vertical: 16),
                  backgroundColor: Colors.blue[600],
                ),
                child: _isLoading 
                  ? CircularProgressIndicator(color: Colors.white)
                  : Text('Submit Assessment', style: TextStyle(fontSize: 18)),
              ),
              
              // Results
              if (_result != null) ...[
                SizedBox(height: 24),
                _buildResultsCard(),
              ],
            ],
          ),
        ),
      ),
    );
  }
  
  Widget _buildSection(String title, List<Widget> children) {
    return Card(
      margin: EdgeInsets.only(bottom: 16),
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              title,
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 16),
            ...children,
          ],
        ),
      ),
    );
  }
  
  Widget _buildResultsCard() {
    final riskLevel = _result!['risk_level'];
    final riskScore = _result!['risk_score'];
    final tips = _result!['tips'];
    
    Color riskColor;
    switch (riskLevel) {
      case 'Low':
        riskColor = Colors.green;
        break;
      case 'Medium':
        riskColor = Colors.orange;
        break;
      case 'High':
        riskColor = Colors.red;
        break;
      default:
        riskColor = Colors.grey;
    }
    
    return Card(
      color: riskColor.withOpacity(0.1),
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.assessment, color: riskColor),
                SizedBox(width: 8),
                Text(
                  'Risk Assessment Results',
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
              ],
            ),
            SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Risk Score', style: TextStyle(fontSize: 14)),
                      Text(
                        '$riskScore/100',
                        style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: riskColor),
                      ),
                    ],
                  ),
                ),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Risk Level', style: TextStyle(fontSize: 14)),
                      Container(
                        padding: EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                        decoration: BoxDecoration(
                          color: riskColor,
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Text(
                          riskLevel,
                          style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            SizedBox(height: 16),
            Text(
              'Health Recommendations',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 8),
            ...(tips['actions'] as List).map((tip) => Padding(
              padding: EdgeInsets.only(bottom: 8),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(Icons.check_circle, color: Colors.green, size: 20),
                  SizedBox(width: 8),
                  Expanded(child: Text(tip)),
                ],
              ),
            )).toList(),
          ],
        ),
      ),
    );
  }
}

## 🔧 Configuration

### Development
```dart
static const String baseUrl = 'http://10.0.2.2:8000'; // Android emulator
// or
static const String baseUrl = 'http://localhost:8000'; // iOS simulator
```

### Production
```dart
static const String baseUrl = 'https://your-api-domain.com';
```

## 📱 Features

- ✅ **Form Validation**: Built-in validation for all fields
- ✅ **Loading States**: Proper loading indicators
- ✅ **Error Handling**: User-friendly error messages
- ✅ **Responsive Design**: Works on all screen sizes
- ✅ **Material Design**: Follows Flutter design guidelines
- ✅ **Real-time Updates**: Immediate feedback on form changes

## 🚀 Next Steps

1. **Customize UI**: Adapt colors, fonts, and layout to match your app
2. **Add Animations**: Smooth transitions between screens
3. **Implement Caching**: Store results locally for offline access
4. **Add Analytics**: Track user interactions and assessment results
5. **Multi-language**: Support for different languages using the `lang` parameter

## 📚 Additional Resources

- [Flutter HTTP Package](https://pub.dev/packages/http)
- [Flutter Form Validation](https://flutter.dev/docs/cookbook/forms/validation)
- [Material Design Guidelines](https://material.io/design)
