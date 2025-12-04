import React, { useEffect, useMemo, useState } from 'react';
import {
  Alert,
  FlatList,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from 'react-native';
import {
  createAvailabilitySlot,
  deleteAvailabilitySlot,
  getMyAvailability,
} from '../../api/student';

interface AvailabilitySlot {
  id: number;
  day_of_week: number;
  start_time: string;
  end_time: string;
}

const dayNames = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar'];

const StudentAvailabilityScreen: React.FC = () => {
  const [slots, setSlots] = useState<AvailabilitySlot[]>([]);
  const [dayOfWeek, setDayOfWeek] = useState<number>(0);
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');

  const fetchSlots = async () => {
    try {
      const response = await getMyAvailability();
      setSlots(response.data);
    } catch (error) {
      Alert.alert('Hata', 'Müsaitlik bilgileri alınamadı.');
    }
  };

  useEffect(() => {
    fetchSlots();
  }, []);

  const isValidTimeRange = useMemo(() => {
    if (!startTime || !endTime) return false;
    const [sh, sm] = startTime.split(':').map(Number);
    const [eh, em] = endTime.split(':').map(Number);
    if (
      Number.isNaN(sh) ||
      Number.isNaN(sm) ||
      Number.isNaN(eh) ||
      Number.isNaN(em) ||
      sm < 0 ||
      sm > 59 ||
      em < 0 ||
      em > 59 ||
      sh < 0 ||
      sh > 23 ||
      eh < 0 ||
      eh > 23
    ) {
      return false;
    }
    return eh * 60 + em > sh * 60 + sm;
  }, [startTime, endTime]);

  const handleAdd = async () => {
    if (!isValidTimeRange) {
      Alert.alert('Uyarı', 'Lütfen geçerli bir saat aralığı girin.');
      return;
    }

    try {
      const response = await createAvailabilitySlot({
        day_of_week: dayOfWeek,
        start_time: startTime,
        end_time: endTime,
      });
      setSlots((prev) => [...prev, response.data]);
      setStartTime('');
      setEndTime('');
    } catch (error) {
      Alert.alert('Hata', 'Müsaitlik eklenemedi.');
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteAvailabilitySlot(id);
      setSlots((prev) => prev.filter((slot) => slot.id !== id));
    } catch (error) {
      Alert.alert('Hata', 'Silme sırasında hata oluştu.');
    }
  };

  const renderSlot = ({ item }: { item: AvailabilitySlot }) => (
    <View style={styles.slotRow}>
      <View>
        <Text style={styles.slotDay}>{dayNames[item.day_of_week]}</Text>
        <Text style={styles.slotTime}>
          {item.start_time} - {item.end_time}
        </Text>
      </View>
      <TouchableOpacity
        style={styles.deleteButton}
        onPress={() => handleDelete(item.id)}
      >
        <Text style={styles.deleteButtonText}>Sil</Text>
      </TouchableOpacity>
    </View>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.sectionTitle}>Mevcut Müsaitlikler</Text>
      <FlatList
        data={slots}
        keyExtractor={(item) => item.id.toString()}
        renderItem={renderSlot}
        ListEmptyComponent={<Text>Müsaitlik bulunmuyor.</Text>}
      />

      <View style={styles.divider} />

      <Text style={styles.sectionTitle}>Yeni Müsaitlik Ekle</Text>
      <View style={styles.dayPicker}>
        {dayNames.map((name, index) => {
          const active = index === dayOfWeek;
          return (
            <TouchableOpacity
              key={name}
              style={[styles.dayButton, active && styles.dayButtonActive]}
              onPress={() => setDayOfWeek(index)}
            >
              <Text style={active ? styles.dayTextActive : styles.dayText}>{name}</Text>
            </TouchableOpacity>
          );
        })}
      </View>

      <Text style={styles.label}>Başlangıç Saati (HH:MM)</Text>
      <TextInput
        value={startTime}
        onChangeText={setStartTime}
        style={styles.input}
        placeholder="Örn: 17:00"
      />

      <Text style={styles.label}>Bitiş Saati (HH:MM)</Text>
      <TextInput
        value={endTime}
        onChangeText={setEndTime}
        style={styles.input}
        placeholder="Örn: 19:00"
      />

      <TouchableOpacity style={styles.addButton} onPress={handleAdd}>
        <Text style={styles.addButtonText}>Ekle</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#fff',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    marginBottom: 12,
  },
  slotRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderColor: '#eee',
  },
  slotDay: {
    fontWeight: '600',
    marginBottom: 4,
  },
  slotTime: {
    color: '#555',
  },
  deleteButton: {
    paddingHorizontal: 12,
    paddingVertical: 8,
    backgroundColor: '#ff6347',
    borderRadius: 8,
  },
  deleteButtonText: {
    color: '#fff',
    fontWeight: '700',
  },
  divider: {
    height: 1,
    backgroundColor: '#eee',
    marginVertical: 16,
  },
  dayPicker: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
    marginBottom: 16,
  },
  dayButton: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 16,
    paddingVertical: 8,
    paddingHorizontal: 10,
  },
  dayButtonActive: {
    backgroundColor: '#1e90ff',
    borderColor: '#1e90ff',
  },
  dayText: {
    color: '#333',
  },
  dayTextActive: {
    color: '#fff',
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
  addButton: {
    backgroundColor: '#1e90ff',
    paddingVertical: 14,
    borderRadius: 8,
    alignItems: 'center',
  },
  addButtonText: {
    color: '#fff',
    fontWeight: '700',
  },
});

export default StudentAvailabilityScreen;
