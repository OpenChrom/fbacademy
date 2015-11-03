package org.eclipse.chemclipse.model.core;

import java.util.List;

public class ISlopes {
	private List<Float> slopes;
	private List<Integer> retentionTimes;
	
	public ISlopes() {
		slopes = new List<Float>();
		retentionTimes = new List<Integer>();
	}
	
	public void setSlopes(List<Float> slopes) {
		this.slopes = slopes;
	}
	
	public void setRetentionTimes(List<Integer> retentionTimes) {
		this.retentionTimes = retentionTimes;
	}
	
	public List<Float> getSlopes() {
		return this.slopes;
	}
	
	public List<Integer> getRetentionTimes() {
		return this.retentionTimes;
	}
}