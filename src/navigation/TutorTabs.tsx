import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import TutorHomeScreen from '../screens/Tutor/TutorHomeScreen';

export type TutorTabsParamList = {
  TutorHome: undefined;
};

const Tab = createBottomTabNavigator<TutorTabsParamList>();

const TutorTabs = () => (
  <Tab.Navigator>
    <Tab.Screen name="TutorHome" component={TutorHomeScreen} options={{ title: 'Ana Sayfa' }} />
  </Tab.Navigator>
);

export default TutorTabs;
