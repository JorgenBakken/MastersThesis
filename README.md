# Masters Thesis 

This repository contains the framework used for the master project by Jørgen Norvik Bakken. 

The work is done is a collaboration with
[Professor Elena Celledoni](https://www.ntnu.edu/employees/elena.celledoni)

It is the continuation of the work done by Pål Erik Lystad and others before him. 
https://github.com/paalel/Signatures-in-Shape-Analysis 

# Structure

## Animation Handling

### animation/src/
- **Skeleton and Animation Objects**: Classes defining the core data structures for animations.
- **Parsing**: Methods to parse `.asf` and `.amc` files.
- **Frame Interpolation**: Utility methods for frame interpolation.

### animation/db/
- **SQLite Database**: Houses the main SQLite database.
- **SQL Scripts**: Contains SQL scripts for table creation and initialization.

---

## Distance Calculations and Clustering

### so3/

#### Core Algorithms
- **signature.py**: Implements signature-based distance calculations.
- **log_signature.py**: Implements log signature-based distance calculations.
- **dynamic_distance.py**: Contains helper functions for dynamic programming-based distance calculations.
- **curves.py**: Central file containing solvers for various types of distance calculations.

#### Utility Files
- **helpers.py**: General-purpose helper functions.
- **convert.py**: Functions for data conversion, e.g., from skeleton to \( SO(3) \).
- **transformations.py**: Functions for data conversion. 

#### Clustering
- **clustering/signature.py**: Clustering based on signature distance.
- **clustering/similarity.py**: Clustering based on various distance metrics.
- **clustering/clustering_so3.R**: (Under Development) Utility for plotting clustering results.
- **clustering/id_set.py**: File extraction and cropping for preprocessing.

---

## Additional Files

### display_animation.py
- Functionality to animate movements based on the library's data structures.

---

## Deprecated or Unused Folders
- **linear/**: Appears to be an older folder and might be considered for deletion.
- **se3/**: Currently empty.


# Setup 
**1.** Create Database Tables: Navigate to the **'animation/db'** directory and run the following command to create the necessary tables: 
```bash 
sqlite3 <Name_of_db>.db < create_tables_sqlite3.sql
```

**2.** Download Data: Obtain mocap data from [CMU Mocap](http://mocap.cs.cmu.edu) and unzip it.

**3.** Configure Paths: Copy the example config file and update the paths:
```bash 
cp db_config_example.py db_config.py
```
&nbsp;&nbsp;&nbsp;&nbsp;Open 'db_config.py' and set the paths to your database and subject folder.

**4.** Populate Database: Run the following command to populate the database and download subject descriptions:
```bash 
python insert_data_db_sqlite3.py
```

# Interacting with the SQLite Database

To interact with the SQLite database **mocap.db**, follow these steps:

1. Open a command prompt or terminal on your computer.
2. Navigate to the `/animation/db` directory using the `cd` command. For example:
   
   ```bash
   cd /path/to/animation/db
   ```
3. Launch the SQLite command-line tool by entering the following command:

   ```bash
   sqlite3 mocap.db
   ```
   You should now see the sqlite> prompt, indicating that you are in the SQLite command-line interface.

4. To exit the SQLite command-line interface, you can either use the .quit command:
   ```bash
   .quit
   ```
   Or you can use the keyboard shortcut Ctrl + C (keyboard interrupt).

## Useful commands
Here are some useful commands you can use while in the SQLite command-line interface:
- To list all the tables in the database, enter:
   ```bash
   .tables
   ```
- To show the contents of the "similarity" table, enter:
   ```bash
   SELECT * FROM similarity;
   ```
- To delete the content in the "similarity" table:
     ```bash
     DELETE FROM similarity;
     ``` 
Feel free to explore the database and interact with the data using these commands. It's a convenient way to verify that the data is being filled correctly and to retrieve information from the database.
   
# Usage 
To display the subject **YY** with the movement **XX** in the database, use the command:
```bash 
python display_animation.py YY XX
```
where YY is the skeleton/character and XX is the movement

## so3

The folder so3/ contains implementation our mathematical framework for SO3.

```convert.py``` : convert animation to curce in SO3.

```transformations.py``` log, exp, interpolate, SRVT and other transformations
applied to SO3 or curves in SO3.

```curves.py```: operations that take a curve, or multiple curves as
parameters. This includes distance, dynamic_distance, close, move_origin and
others. These are all written to be functional in style.

```dynamic_distance.py```: implementations off the the dynamic distance method
proposed by Bauer.

```signature.py and log_signature.py```: proposed metrics, calculated for
geodesic interpolation curves using the iisignature library.


the folders ```experiments/``` and ```clustering/``` contain different
applications of these methods.  

## se3

Transformations applied to the group SE(3), the above mentioned framework could
be applied to this group using a similar approach.

