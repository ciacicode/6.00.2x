# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 

import numpy
import random
import pylab
import pdb

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 2
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """

        if random.random() < self.getClearProb():
            return True
        else:
            return False

    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        if random.random() < self.maxBirthProb * (1-popDensity):
            # reproduce
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException



class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """

        return int(len(self.getViruses()))


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """

        dead_viruses = list()
        offspring_viruses = list()
        current_viruses = self.getViruses()
        for virus in current_viruses:
            if virus.doesClear():
                dead_viruses.append(virus)
        # update list of viruses by removing dead viruses
        for dead_virus in dead_viruses:
            current_viruses.remove(dead_virus)

        popDensity = float(len(current_viruses))/float(self.getMaxPop())

        for survived_virus in current_viruses:
            try:
                offspring = survived_virus.reproduce(popDensity)
                offspring_viruses.append(offspring)
            except NoChildException:
                pass
        # update list of viruses with the new offsprint
            self.viruses = current_viruses + offspring_viruses

        return self.getTotalPop()





#
# PROBLEM 3
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """

    step_viruses_list = list()
    time_steps = 300
    # creates a dictionary where to track total viruses at given steps
    for step in range(time_steps):
            step_viruses_list.append(0.0)

    for trial in range(numTrials):
        viruses = list()
        for virus in range(numViruses):
        # instantiate viruses and append them to a list
            new_virus = SimpleVirus(maxBirthProb, clearProb)
            viruses.append(new_virus)

        # instantiates a patient
        patient = Patient(viruses, maxPop)

        for step in range(time_steps):
            step_viruses_list[step] = float(step_viruses_list[step])+float(patient.update())

    # calculate average total viruses per step
    for virus_count in range(len(step_viruses_list)):
        average = float(step_viruses_list[virus_count])/float(numTrials)
        step_viruses_list[virus_count] = average

    pylab.plot(step_viruses_list, label="average virus population")
    pylab.title("Average virus population by time step")
    pylab.xlabel("Steps")
    pylab.ylabel("Average Virus Population")
    pylab.legend(loc='upper right')
    pylab.show()






#
# PROBLEM 4
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """

        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb


    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        if drug in self.getResistances().keys():
            return self.getResistances()[drug]
        else:
            return False


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """

        #check that there is no active drug to which the virus is not resistant to

        if len(activeDrugs) > 0:
            for drug in activeDrugs:
                if drug in self.getResistances().keys():
                    #check that this doesn't have value False
                    if self.getResistances()[drug] is False:
                        #no chance of reproduction
                        raise NoChildException
                    else:
                        pass
        else:
            pass

        new_resistance = dict()
        for drug in self.getResistances().keys():
            if random.random() < (1 - self.getMutProb()):
                #inherits same trait of parent
                new_resistance[drug] = self.getResistances()[drug]
            else:
                #changes trait
                new_resistance[drug] = not self.getResistances()[drug]

        #if we are here no exception was raised, meaning the virus is resistant to all active drugs
        if random.random() < self.maxBirthProb * (1-popDensity):
            # reproduce
            return ResistantVirus(self.maxBirthProb, self.clearProb, new_resistance, self.mutProb)
        else:
            raise NoChildException



            

class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """

        Patient.__init__(self, viruses, maxPop)
        self.prescribedDrugs = list()


    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        if newDrug not in self.prescribedDrugs:
            self.prescribedDrugs.append(newDrug)

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.prescribedDrugs


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """

        virus_population = self.getViruses()
        resistant_count = 0
        for virus in virus_population:
            bool_check = list()
            for drug in drugResist:
                if virus.isResistantTo(drug) is True:
                    bool_check.append(True)
                else:
                    bool_check.append(False)
            if False in bool_check:
                pass
            else:
                resistant_count+=1
        return resistant_count

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """

        dead_viruses = list()
        offspring_viruses = list()
        current_viruses = self.getViruses()
        for virus in current_viruses:
            if virus.doesClear():
                dead_viruses.append(virus)
        # update list of viruses by removing dead viruses
        for dead_virus in dead_viruses:
            current_viruses.remove(dead_virus)

        popDensity = float(len(current_viruses))/float(self.getMaxPop())

        for survived_virus in current_viruses:
            try:
                offspring = survived_virus.reproduce(popDensity, self.getPrescriptions())
                offspring_viruses.append(offspring)
            except NoChildException:
                pass
        # update list of viruses with the new offsprint
            self.viruses = current_viruses + offspring_viruses

        return self.getTotalPop()



#
# PROBLEM 5
#
def simulationWithDrug(numTrials, timesteps_nodrug, numViruses = 100, maxPop= 1000, maxBirthProb = 0.1, clearProb = 0.05, resistances = {'guttagonol': False},
                       mutProb=0.005,timesteps_afterdrug = 150,  ):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """

    step_viruses_any = list()
    step_viruses_resistant = list()
    trial_viruses = list()
    time_steps = timesteps_nodrug + timesteps_afterdrug
    # creates a dictionary where to track total and resistant viruses at given steps
    for step in range(time_steps):
            step_viruses_any.append(0.0)
            step_viruses_resistant.append(0.0)

    for trial in range(numTrials):
        viruses = list()
        for virus in range(numViruses):
        # instantiate viruses and append them to a list
            new_virus = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
            viruses.append(new_virus)

        # instantiates a patient
        patient = TreatedPatient(viruses, maxPop)

        for step in range(time_steps):
            if step < timesteps_nodrug:
                # step_viruses_any[step] = float(step_viruses_any[step])+float(patient.update())
                # step_viruses_resistant[step] = float(step_viruses_resistant[step]) + float(patient.getResistPop(['guttagonol']))
                step_viruses_any[step] = float(patient.update())
            else:
                patient.addPrescription('guttagonol')
                # step_viruses_any[step] = float(step_viruses_any[step])+float(patient.update())
                # step_viruses_resistant[step] = float(step_viruses_resistant[step]) + float(patient.getResistPop(['guttagonol']))
                step_viruses_any[step] = float(patient.update())
    # calculate average total viruses per step

    # for virus_count in range(len(step_viruses_any)):
    #     any_virus_average = float(step_viruses_any[virus_count])/float(numTrials)
    #     resistant_virus_average = float(step_viruses_resistant[virus_count]/float(numTrials))
    #     step_viruses_any[virus_count] = any_virus_average
    #     step_viruses_resistant[virus_count] = resistant_virus_average

        # get final virus population
        trial_viruses.append((trial, step_viruses_any[-1]))
        # identify total virus population per trial

    return trial_viruses

def simulationWithMultipleDrug(numTrials, timesteps_firstdrug, numViruses = 100, maxPop= 1000, maxBirthProb = 0.2, clearProb = 0.05, resistances = {'guttagonol': False, 'grimpex': False},
                       mutProb=0.01,timesteps_afterdrug = 150, timesteps_nodrug= 150 ):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1).
    numTrials: number of simulation runs to execute (an integer)

    """

    step_viruses_any = list()
    step_viruses_resistant = list()
    trial_viruses = list()
    time_steps = timesteps_nodrug + timesteps_afterdrug + timesteps_firstdrug
    # creates a dictionary where to track total and resistant viruses at given steps
    for step in range(time_steps):
            step_viruses_any.append(0.0)
            step_viruses_resistant.append(0.0)

    for trial in range(numTrials):
        viruses = list()
        for virus in range(numViruses):
        # instantiate viruses and append them to a list
            new_virus = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
            viruses.append(new_virus)

        # instantiates a patient
        patient = TreatedPatient(viruses, maxPop)

        for step in range(time_steps):
            if step < timesteps_nodrug:
                step_viruses_any[step] = float(patient.update())
            elif step > timesteps_firstdrug:
                patient.addPrescription('guttagonol')
                step_viruses_any[step] = float(patient.update())
            else:
                patient.addPrescription('grimpex')
                step_viruses_any[step] = float(patient.update())

        # get final virus population
        trial_viruses.append(step_viruses_any[-1])
        # identify total virus population per trial

    return trial_viruses