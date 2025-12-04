import React, { useEffect, useState } from 'react';
import {
  Alert,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from 'react-native';
import { Picker } from '@react-native-picker/picker';
import axios from 'axios';
import {
  StudentProfilePayload,
  getStudentProfile,
  upsertStudentProfile,
} from '../../api/student';

const gradeOptions: { label: string; value: StudentProfilePayload['grade'] }[] = [
  { label: '11', value: '11' },
  { label: '12', value: '12' },
  { label: 'Mezun', value: 'graduate' },
];

const examOptions: { label: string; value: StudentProfilePayload['target_exam'] }[] = [
  { label: 'TYT', value: 'TYT' },
  { label: 'AYT', value: 'AYT' },
  { label: 'TYT+AYT', value: 'BOTH' },
];

const modeOptions = [
  { label: 'Online', value: 'online' },
  { label: 'Öğrenci evi', value: 'student_home' },
  { label: 'Hibrit', value: 'hybrid' },
];

const StudentProfileScreen: React.FC = () => {
  const [fullName, setFullName] = useState('');
  const [grade, setGrade] = useState<StudentProfilePayload['grade']>('11');
  const [targetExam, setTargetExam] =
    useState<StudentProfilePayload['target_exam']>('TYT');
  const [targetScore, setTargetScore] = useState<string>('');
  const [targetRank, setTargetRank] = useState<string>('');
  const [district, setDistrict] = useState('');
  const [neighborhood, setNeighborhood] = useState('');
  const [preferredModes, setPreferredModes] = useState<string[]>([]);
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(true);
  const [savedMessage, setSavedMessage] = useState('');

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await getStudentProfile();
        const data = response.data;
        setFullName(data.full_name || '');
        setGrade(data.grade || '11');
        setTargetExam(data.target_exam || 'TYT');
        setTargetScore(data.target_score ? String(data.target_score) : '');
        setTargetRank(data.target_rank ? String(data.target_rank) : '');
        setDistrict(data.district || '');
        setNeighborhood(data.neighborhood || '');
        setPreferredModes(data.preferred_modes || []);
        setNotes(data.notes || '');
      } catch (error) {
        if (axios.isAxiosError(error) && error.response?.status === 404) {
          // leave form empty
        } else {
          Alert.alert('Hata', 'Profil getirilirken hata oluştu.');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  const toggleMode = (value: string) => {
    setPreferredModes((prev) =>
      prev.includes(value) ? prev.filter((m) => m !== value) : [...prev, value],
    );
  };

  const handleSave = async () => {
    const payload: StudentProfilePayload = {
      full_name: fullName,
      grade,
      target_exam: targetExam,
      target_score: targetScore ? Number(targetScore) : null,
      target_rank: targetRank ? Number(targetRank) : null,
      city: 'Istanbul',
      district,
      neighborhood: neighborhood || null,
      preferred_modes: preferredModes,
      notes: notes || null,
    };

    try {
      await upsertStudentProfile(payload);
      setSavedMessage('Kaydedildi');
      Alert.alert('Başarılı', 'Kaydedildi');
    } catch (error) {
      Alert.alert('Hata', 'Kaydetme sırasında bir hata oluştu.');
    }
  };

  if (loading) {
    return (
      <View style={styles.centered}>
        <Text>Yükleniyor...</Text>
      </View>
    );
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.label}>Ad Soyad</Text>
      <TextInput
        value={fullName}
        onChangeText={setFullName}
        style={styles.input}
        placeholder="Ad Soyad"
      />

      <Text style={styles.label}>Sınıf</Text>
      <View style={styles.pickerWrapper}>
        <Picker selectedValue={grade} onValueChange={(val) => setGrade(val)}>
          {gradeOptions.map((option) => (
            <Picker.Item
              key={option.value}
              label={option.label}
              value={option.value}
            />
          ))}
        </Picker>
      </View>

      <Text style={styles.label}>Hedef Sınav</Text>
      <View style={styles.pickerWrapper}>
        <Picker
          selectedValue={targetExam}
          onValueChange={(val) => setTargetExam(val)}
        >
          {examOptions.map((option) => (
            <Picker.Item
              key={option.value}
              label={option.label}
              value={option.value}
            />
          ))}
        </Picker>
      </View>

      <Text style={styles.label}>Hedef Puan</Text>
      <TextInput
        value={targetScore}
        onChangeText={setTargetScore}
        style={styles.input}
        placeholder="Örn: 450"
        keyboardType="numeric"
      />

      <Text style={styles.label}>Hedef Sıralama</Text>
      <TextInput
        value={targetRank}
        onChangeText={setTargetRank}
        style={styles.input}
        placeholder="Örn: 5000"
        keyboardType="numeric"
      />

      <Text style={styles.label}>Şehir</Text>
      <TextInput value="İstanbul" editable={false} style={styles.input} />

      <Text style={styles.label}>İlçe</Text>
      <TextInput
        value={district}
        onChangeText={setDistrict}
        style={styles.input}
        placeholder="İlçe"
      />

      <Text style={styles.label}>Mahalle</Text>
      <TextInput
        value={neighborhood}
        onChangeText={setNeighborhood}
        style={styles.input}
        placeholder="Mahalle"
      />

      <Text style={styles.label}>Ders tipi tercihleri</Text>
      <View style={styles.modeContainer}>
        {modeOptions.map((option) => {
          const active = preferredModes.includes(option.value);
          return (
            <TouchableOpacity
              key={option.value}
              style={[styles.modeButton, active && styles.modeButtonActive]}
              onPress={() => toggleMode(option.value)}
            >
              <Text style={active ? styles.modeTextActive : styles.modeText}>
                {option.label}
              </Text>
            </TouchableOpacity>
          );
        })}
      </View>

      <Text style={styles.label}>Notlar</Text>
      <TextInput
        value={notes}
        onChangeText={setNotes}
        style={[styles.input, styles.textArea]}
        placeholder="Notlar"
        multiline
        numberOfLines={4}
      />

      <TouchableOpacity style={styles.saveButton} onPress={handleSave}>
        <Text style={styles.saveButtonText}>Kaydet</Text>
      </TouchableOpacity>

      {savedMessage ? <Text style={styles.savedText}>{savedMessage}</Text> : null}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 16,
    backgroundColor: '#fff',
  },
  label: {
    fontWeight: '600',
    marginBottom: 6,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    padding: 12,
    marginBottom: 16,
  },
  pickerWrapper: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    marginBottom: 16,
  },
  modeContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
    marginBottom: 16,
  },
  modeButton: {
    paddingVertical: 10,
    paddingHorizontal: 14,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#ccc',
  },
  modeButtonActive: {
    backgroundColor: '#1e90ff',
    borderColor: '#1e90ff',
  },
  modeText: {
    color: '#333',
  },
  modeTextActive: {
    color: '#fff',
  },
  textArea: {
    height: 120,
    textAlignVertical: 'top',
  },
  saveButton: {
    backgroundColor: '#1e90ff',
    paddingVertical: 14,
    borderRadius: 8,
    alignItems: 'center',
  },
  saveButtonText: {
    color: '#fff',
    fontWeight: '700',
  },
  savedText: {
    marginTop: 12,
    color: 'green',
    textAlign: 'center',
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default StudentProfileScreen;
