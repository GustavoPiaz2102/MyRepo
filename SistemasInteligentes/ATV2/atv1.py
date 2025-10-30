from ucimlrepo import fetch_ucirepo
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

heart_disease = fetch_ucirepo(id=45)

X = heart_disease.data.features
y = heart_disease.data.targets.values.ravel()  

#Separar

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)



clf = DecisionTreeClassifier(max_depth=4, random_state=42) 
clf.fit(X_train, y_train)

acc = clf.score(X_test, y_test)
print(f"Acurácia no teste: {acc:.2f}")


importances = clf.feature_importances_
for i in importances:
    print(f"\n {i}")

#Plotar
plt.figure(figsize=(20, 10))
plot_tree(
    clf,
    feature_names=X.columns,
    class_names=[str(c) for c in clf.classes_],
    filled=True,
    rounded=True,
    fontsize=10
)
plt.show()
