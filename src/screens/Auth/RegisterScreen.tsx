import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';
import { NavigationProp, ParamListBase, useNavigation } from '@react-navigation/native';
import { register as registerUser } from '../../api/auth';
import authStore from '../../store/authStore';

const RegisterScreen: React.FC = () => {
  const navigation = useNavigation<NavigationProp<ParamListBase>>();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState<'student' | 'tutor'>('student');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleRegister = async () => {
    setLoading(true);
    setError('');
    try {
      const { user, token } = await registerUser({ email, password, role });
      authStore.setAuth(token, user);
      navigation.reset({
        index: 0,
        routes: [{ name: user.role === 'student' ? 'StudentTabs' : 'TutorTabs' }],
      });
    } catch (err: any) {
      const message = err?.response?.data?.message || 'Bir hata oluştu. Lütfen tekrar deneyin.';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Hesap Oluştur</Text>

      <Text style={styles.label}>E-posta</Text>
      <TextInput
        style={styles.input}
        placeholder="ornek@mail.com"
        autoCapitalize="none"
        keyboardType="email-address"
        value={email}
        onChangeText={setEmail}
      />

      <Text style={styles.label}>Şifre</Text>
      <TextInput
        style={styles.input}
        placeholder="••••••••"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />

      <Text style={styles.label}>Rol</Text>
      <View style={styles.roleContainer}>
        <TouchableOpacity
          style={[styles.roleButton, role === 'student' && styles.roleButtonActive]}
          onPress={() => setRole('student')}
        >
          <Text style={[styles.roleText, role === 'student' && styles.roleTextActive]}>Öğrenciyim</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.roleButton, role === 'tutor' && styles.roleButtonActive]}
          onPress={() => setRole('tutor')}
        >
          <Text style={[styles.roleText, role === 'tutor' && styles.roleTextActive]}>
            Özel ders veriyorum
          </Text>
        </TouchableOpacity>
      </View>

      {error ? <Text style={styles.error}>{error}</Text> : null}

      <TouchableOpacity
        style={[styles.submitButton, loading && styles.submitButtonDisabled]}
        onPress={handleRegister}
        disabled={loading}
      >
        <Text style={styles.submitText}>{loading ? 'Kaydediliyor...' : 'Kayıt Ol'}</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 24,
    backgroundColor: '#ffffff',
    justifyContent: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: '700',
    marginBottom: 24,
    textAlign: 'center',
    color: '#111827',
  },
  label: {
    fontSize: 14,
    color: '#374151',
    marginBottom: 8,
  },
  input: {
    borderWidth: 1,
    borderColor: '#d1d5db',
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    marginBottom: 16,
    fontSize: 16,
    color: '#111827',
  },
  roleContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 16,
  },
  roleButton: {
    flex: 1,
    paddingVertical: 12,
    paddingHorizontal: 10,
    borderWidth: 1,
    borderColor: '#d1d5db',
    borderRadius: 8,
    marginRight: 8,
    alignItems: 'center',
    justifyContent: 'center',
  },
  roleButtonActive: {
    borderColor: '#2563eb',
    backgroundColor: '#eff6ff',
  },
  roleText: {
    fontSize: 14,
    color: '#374151',
  },
  roleTextActive: {
    color: '#1d4ed8',
    fontWeight: '600',
  },
  error: {
    color: '#dc2626',
    marginBottom: 12,
    textAlign: 'center',
  },
  submitButton: {
    backgroundColor: '#2563eb',
    paddingVertical: 14,
    borderRadius: 10,
    alignItems: 'center',
  },
  submitButtonDisabled: {
    opacity: 0.7,
  },
  submitText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '700',
  },
});

export default RegisterScreen;
